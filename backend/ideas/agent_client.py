import os
import requests
import time
from django.conf import settings

AGENTS_BASE_URL = os.getenv('AGENTS_BASE_URL', settings.AGENTS_BASE_URL)

class AgentClient:
    """
    Adapter for CrewAI Validation API
    
    Maps Django session model to CrewAI validation requests
    """
    def __init__(self, base_url=None):
        self.base = base_url or AGENTS_BASE_URL.rstrip('/')

    def start_session(self, session):
        """
        Start CrewAI validation process
        
        Maps Django session to CrewAI ValidationRequest format
        """
        url = f"{self.base}/api/v1/validate"
        
        # Convert Django session to CrewAI format
        payload = {
            "topic": session.idea.description,
            "user_context": {
                "business_idea": session.idea.description,
                "title": session.idea.title,
                "user_id": str(session.idea.owner.id),
                "session_id": str(session.id),
                "target_market": getattr(session.idea, 'target_market', ''),
                "budget": getattr(session.idea, 'budget', 0),
                "timeline": getattr(session.idea, 'timeline', '')
            },
            "webhook_url": None  # We'll poll for results instead
        }
        
        try:
            r = requests.post(url, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            
            # Store CrewAI execution_id as agent_run_id
            if 'execution_id' in data:
                session.agent_run_id = data['execution_id']
                session.save()
                
                # Start polling for results in background
                self._poll_for_results(session, data['execution_id'])
            
            return data
            
        except requests.RequestException as e:
            from .models import Message
            Message.objects.create(
                session=session, 
                sender=Message.SENDER_SYSTEM,
                content=f"Failed to start AI validation: {e}", 
                metadata={"error": str(e)}
            )
            return {"error": str(e)}

    def _poll_for_results(self, session, execution_id):
        """
        Poll CrewAI for validation results
        """
        from .models import Message
        
        # Send initial message
        Message.objects.create(
            session=session,
            sender=Message.SENDER_AGENT,
            content="🚀 Начинаю анализ вашей бизнес-идеи с помощью AI-агентов...",
            metadata={"type": "status", "execution_id": execution_id}
        )
        
        max_attempts = 60  # 10 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Check status
                status_url = f"{self.base}/api/v1/status/{execution_id}"
                response = requests.get(status_url, timeout=10)
                
                if response.status_code == 200:
                    status_data = response.json()
                    
                    if status_data['status'] == 'completed':
                        # Get final results
                        result_url = f"{self.base}/api/v1/result/{execution_id}"
                        result_response = requests.get(result_url, timeout=10)
                        
                        if result_response.status_code == 200:
                            result_data = result_response.json()
                            
                            # Create final report message
                            Message.objects.create(
                                session=session,
                                sender=Message.SENDER_AGENT,
                                content="✅ Анализ завершен! Вот ваш подробный отчет:",
                                metadata={
                                    "type": "final_report",
                                    "execution_id": execution_id
                                }
                            )
                            
                            # Store report in session
                            session.report = result_data.get('final_report_markdown', '')
                            session.report_sections = [{
                                'title': 'AI Validation Report',
                                'html': result_data.get('final_report_markdown', '').replace('\n', '<br>')
                            }]
                            session.finished = True
                            session.save()
                            
                        break
                        
                    elif status_data['status'] == 'failed':
                        Message.objects.create(
                            session=session,
                            sender=Message.SENDER_SYSTEM,
                            content="❌ Произошла ошибка при анализе бизнес-идеи",
                            metadata={
                                "type": "error",
                                "error": status_data.get('error_message', 'Unknown error')
                            }
                        )
                        break
                        
                    else:
                        # Still running - send progress update
                        agents_completed = status_data.get('agents_completed', 0)
                        total_agents = status_data.get('total_agents', 11)
                        current_stage = status_data.get('current_stage', 'Processing...')
                        
                        progress_message = f"🔄 Анализ в процессе: {agents_completed}/{total_agents} агентов завершили работу\n{current_stage}"
                        
                        Message.objects.create(
                            session=session,
                            sender=Message.SENDER_AGENT,
                            content=progress_message,
                            metadata={
                                "type": "progress",
                                "execution_id": execution_id,
                                "progress": agents_completed / total_agents if total_agents > 0 else 0
                            }
                        )
                
                attempt += 1
                time.sleep(10)  # Wait 10 seconds before next check
                
            except Exception as e:
                attempt += 1
                if attempt >= max_attempts:
                    Message.objects.create(
                        session=session,
                        sender=Message.SENDER_SYSTEM,
                        content=f"❌ Превышено время ожидания результатов: {e}",
                        metadata={"type": "timeout_error"}
                    )
                time.sleep(10)

    def send_user_message(self, session, message):
        """
        Handle user messages during validation
        
        Since CrewAI runs autonomously, we just acknowledge the message
        """
        from .models import Message
        
        # For now, just acknowledge - CrewAI doesn't support mid-process messages
        Message.objects.create(
            session=session,
            sender=Message.SENDER_AGENT,
            content="📝 Сообщение получено! Анализ продолжается автоматически, результаты будут готовы в ближайшее время.",
            metadata={
                "type": "acknowledgment",
                "user_message_id": message.id
            }
        )
        
        return {"status": "acknowledged"}
from celery import shared_task
from .models import Session, Message
from .agent_client import AgentClient
import logging

logger = logging.getLogger(__name__)

@shared_task
def start_session_task(session_id):
    """Start AI validation session in background"""
    try:
        session = Session.objects.get(id=session_id)
        agent_client = AgentClient()
        result = agent_client.start_session(session)
        logger.info(f"Started session {session_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to start session {session_id}: {e}")
        # Create error message
        try:
            session = Session.objects.get(id=session_id)
            Message.objects.create(
                session=session,
                sender=Message.SENDER_SYSTEM,
                content=f"Failed to start AI validation: {str(e)}",
                metadata={"error": str(e), "task": "start_session"}
            )
        except:
            pass
        return {"error": str(e)}

@shared_task
def send_user_message_task(session_id, message_id):
    """Forward user message to AI agents"""
    try:
        session = Session.objects.get(id=session_id)
        message = Message.objects.get(id=message_id)
        agent_client = AgentClient()
        result = agent_client.send_user_message(session, message)
        logger.info(f"Sent message {message_id} to session {session_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send message {message_id} to session {session_id}: {e}")
        return {"error": str(e)}
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
import uuid
import logging
import traceback

from .models import (
    ValidationRequest, ValidationResponse, ValidationStatus, 
    ValidationResult, ErrorResponse, HealthResponse, UserContext
)
from .crew import ValidityCrew
from .database import (
    get_db, create_tables, ValidationExecution, AgentResult, ValidationMetrics,
    ExecutionStatus, AgentStatus, AgentStage
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Business Validation AI Engine",
    description="Multi-agent AI system for comprehensive business idea validation using CrewAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    await create_tables()
    logger.info("🚀 Business Validation AI Engine started successfully")
    logger.info("📊 Database tables created/verified")
    logger.info("🤖 11 AI agents ready for business validation")


async def run_validation_crew(execution_id: str, user_context: UserContext, topic: str):
    """Background task to run the validation crew"""
    from .database import async_session_maker
    
    async with async_session_maker() as session:
        try:
            # Get the execution record
            result = await session.execute(
                select(ValidationExecution).where(ValidationExecution.execution_id == execution_id)
            )
            execution = result.scalar_one()
            
            # Update status to running
            execution.status = ExecutionStatus.RUNNING
            execution.started_at = datetime.now()
            await session.commit()
            
            logger.info(f"🚀 Starting validation for execution_id: {execution_id}")
            
            # Prepare inputs for the crew
            inputs = {
                'topic': topic,
                'user_context': user_context.dict(),
                'current_year': str(datetime.now().year)
            }
            
            # Run the crew
            crew_instance = ValidityCrew()
            result = crew_instance.crew().kickoff(inputs=inputs)
            
            # Store the result
            execution.status = ExecutionStatus.COMPLETED
            execution.completed_at = datetime.now()
            execution.final_report = {
                "raw_result": str(result),
                "summary": "Validation completed successfully",
                "recommendations": []
            }
            execution.final_report_markdown = str(result)
            
            # Create metrics record
            metrics = ValidationMetrics(
                execution_id=execution_id,
                agents_count=11,
                total_tokens_used=0,  # Will be updated based on actual usage
                report_completeness_score=100
            )
            session.add(metrics)
            
            await session.commit()
            logger.info(f"✅ Validation completed for execution_id: {execution_id}")
            
        except Exception as e:
            logger.error(f"❌ Validation failed for execution_id: {execution_id}, error: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Update status to failed
            execution.status = ExecutionStatus.FAILED
            execution.completed_at = datetime.now()
            execution.error_message = str(e)
            await session.commit()


@app.post("/api/v1/validate", response_model=ValidationResponse)
async def start_validation(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Start business idea validation process
    
    This endpoint initiates a comprehensive business validation using 11 specialized AI agents:
    1. Requirements Analyst
    2. Market Researcher  
    3. Competition Analyst
    4. Financial Projector
    5. Risk Assessor
    6. Product Validator
    7. Operations Analyst
    8. Marketing Strategist
    9. Technology Assessor
    10. Legal Advisor
    11. Report Generator
    """
    try:
        execution_id = str(uuid.uuid4())
        
        # Create execution record in database
        execution = ValidationExecution(
            execution_id=execution_id,
            status=ExecutionStatus.PENDING,
            user_context=request.user_context.dict(),
            topic=request.topic,
            webhook_url=request.webhook_url,
            created_at=datetime.now()
        )
        
        db.add(execution)
        await db.commit()
        await db.refresh(execution)
        
        # Add background task
        background_tasks.add_task(
            run_validation_crew, 
            execution_id, 
            request.user_context, 
            request.topic
        )
        
        logger.info(f"🎯 Started validation process: {execution_id}")
        
        return ValidationResponse(
            execution_id=execution_id,
            status="started",
            estimated_duration_minutes=20
        )
        
    except Exception as e:
        logger.error(f"Failed to start validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/status/{execution_id}", response_model=ValidationStatus)
async def get_validation_status(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get validation status and progress
    
    Returns current status, progress information, and any error messages
    for a specific validation execution.
    """
    # Get execution from database
    result = await db.execute(
        select(ValidationExecution).where(ValidationExecution.execution_id == execution_id)
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    # Count completed agents
    agents_result = await db.execute(
        select(func.count(AgentResult.id))
        .where(AgentResult.execution_id == execution_id)
        .where(AgentResult.status == AgentStatus.COMPLETED)
    )
    agents_completed = agents_result.scalar() or 0
    
    return ValidationStatus(
        execution_id=execution_id,
        status=execution.status.value,
        created_at=execution.created_at,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
        agents_completed=agents_completed,
        total_agents=11,
        current_stage=f"Stage: {execution.status.value}",
        error_message=execution.error_message
    )


@app.get("/api/v1/result/{execution_id}", response_model=ValidationResult)
async def get_validation_result(execution_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get validation results
    
    Returns the complete validation report including analysis from all 11 AI agents,
    recommendations, and structured insights.
    """
    # Get execution from database
    result = await db.execute(
        select(ValidationExecution).where(ValidationExecution.execution_id == execution_id)
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    if execution.status != ExecutionStatus.COMPLETED:
        raise HTTPException(
            status_code=400, 
            detail=f"Validation not completed. Current status: {execution.status.value}"
        )
    
    return ValidationResult(
        execution_id=execution_id,
        status=execution.status.value,
        final_report=execution.final_report or {},
        final_report_markdown=execution.final_report_markdown or "",
        created_at=execution.created_at,
        completed_at=execution.completed_at
    )


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns service status and version information.
    """
    return HealthResponse()


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            message="Internal server error",
            details={"error": str(exc)}
        ).dict()
    )
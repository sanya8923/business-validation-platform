from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
import uuid


class UserContext(BaseModel):
    """User context for business idea validation"""
    idea_description: str = Field(..., description="Description of the business idea")
    target_market: str = Field(..., description="Target market (e.g. USA, Russian market, English-speaking)")
    target_audience: str = Field(..., description="Target audience description")
    audience_pains: str = Field(..., description="Audience pains/problems")
    unique_selling_point: str = Field(..., description="Unique selling point")
    programming_skills: Literal["can_code", "use_ai_for_coding", "use_no_code", "cannot_code"] = Field(..., description="Programming skill level")
    has_team: bool = Field(..., description="Whether user has a team")
    team_members: Optional[str] = Field(None, description="Team members description if has_team is True")
    financial_resources: Literal["own_funds", "investor", "credit_planned", "none"] = Field(..., description="Available financial resources")
    available_time_per_week: str = Field(..., description="Available time per week")
    social_media_presence: str = Field(..., description="Social media presence: platforms, audience size, blog topics")


class ValidationRequest(BaseModel):
    """Request to start business idea validation"""
    user_context: UserContext = Field(..., description="User context with business idea details")
    topic: str = Field(..., description="Topic/keyword for research")
    webhook_url: Optional[str] = Field(None, description="Optional webhook URL for completion notification")


class ValidationResponse(BaseModel):
    """Response after starting validation"""
    execution_id: str = Field(..., description="Unique execution ID")
    status: Literal["started"] = Field("started", description="Validation status")
    estimated_duration_minutes: int = Field(20, description="Estimated duration in minutes")


class ValidationStatus(BaseModel):
    """Validation execution status"""
    execution_id: str = Field(..., description="Unique execution ID")
    status: Literal["pending", "running", "completed", "failed"] = Field(..., description="Current status")
    created_at: datetime = Field(..., description="Creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    agents_completed: int = Field(0, description="Number of agents completed")
    total_agents: int = Field(11, description="Total number of agents")
    current_stage: str = Field("", description="Current processing stage")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class ValidationResult(BaseModel):
    """Final validation result"""
    execution_id: str = Field(..., description="Unique execution ID")
    status: Literal["completed"] = Field("completed", description="Validation status")
    final_report: Dict[str, Any] = Field(..., description="Structured final report")
    final_report_markdown: str = Field(..., description="Final report in Markdown format")
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: datetime = Field(..., description="Completion timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response"""
    status: Literal["healthy"] = Field("healthy", description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    version: str = Field("1.0.0", description="API version")
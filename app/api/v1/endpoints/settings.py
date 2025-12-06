"""
Settings endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.settings import (
    ProfileUpdate, VoiceSettingsUpdate, NotificationSettingsUpdate,
    PasswordChange, TwoFactorSetup, TwoFactorVerify, Session,
    BillingInfo, PaymentMethodUpdate, Invoice, ApiKey, ApiKeyCreate,
    Webhook, WebhookCreate, WebhookUpdate
)
from pydantic import BaseModel

router = APIRouter()


@router.put("/profile")
async def update_profile(profile: ProfileUpdate):
    """Update user profile"""
    # TODO: Implement actual profile update
    return {
        "success": True,
        "message": "Profile updated successfully",
        **profile.model_dump(exclude_unset=True)
    }


@router.put("/voice")
async def update_voice_settings(settings: VoiceSettingsUpdate):
    """Update voice settings"""
    # TODO: Implement actual voice settings update
    return {
        "success": True,
        "message": "Voice settings updated successfully",
        **settings.model_dump(exclude_unset=True)
    }


@router.put("/notifications")
async def update_notification_settings(settings: NotificationSettingsUpdate):
    """Update notification settings"""
    # TODO: Implement actual notification settings update
    return {
        "success": True,
        "message": "Notification settings updated successfully",
        **settings.model_dump()
    }


@router.post("/password/change")
async def change_password(request: PasswordChange):
    """Change user password"""
    # TODO: Implement actual password change logic
    if len(request.current_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    if len(request.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters"
        )
    
    return {
        "success": True,
        "message": "Password changed successfully"
    }


@router.post("/2fa/enable", response_model=TwoFactorSetup)
async def enable_2fa():
    """Enable two-factor authentication"""
    # TODO: Implement actual 2FA setup
    return TwoFactorSetup(
        secret="JBSWY3DPEHPK3PXP",
        qr_code="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzAwMCIvPjwvc3ZnPg=="
    )


@router.post("/2fa/disable")
async def disable_2fa():
    """Disable two-factor authentication"""
    # TODO: Implement actual 2FA disable
    return {
        "success": True,
        "message": "2FA disabled successfully"
    }


@router.post("/2fa/verify")
async def verify_2fa(request: TwoFactorVerify):
    """Verify two-factor authentication code"""
    # TODO: Implement actual 2FA verification
    if len(request.code) != 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    return {
        "success": True,
        "message": "2FA verified successfully"
    }


@router.get("/sessions", response_model=List[Session])
async def get_active_sessions():
    """Get active user sessions"""
    # TODO: Implement actual session retrieval
    return [
        Session(
            id="1",
            device="Chrome on Windows",
            location="San Francisco, CA",
            last_active="Active now",
            current=True
        ),
        Session(
            id="2",
            device="Safari on iPhone",
            location="San Francisco, CA",
            last_active="2 hours ago",
            current=False
        ),
    ]


@router.delete("/sessions/{session_id}")
async def revoke_session(session_id: str):
    """Revoke a user session"""
    # TODO: Implement actual session revocation
    return {
        "success": True,
        "message": f"Session {session_id} revoked successfully"
    }


@router.get("/billing", response_model=BillingInfo)
async def get_billing_info():
    """Get billing information"""
    # TODO: Implement actual billing info retrieval
    return BillingInfo(
        plan="Professional",
        status="active",
        next_billing_date="2024-08-15",
        amount="$99.00",
        payment_method={
            "type": "card",
            "last4": "4242",
            "expiry": "12/25"
        }
    )


@router.put("/billing/payment-method")
async def update_payment_method(request: PaymentMethodUpdate):
    """Update payment method"""
    # TODO: Implement actual payment method update
    if len(request.card_number) < 16:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid card number"
        )
    
    return {
        "success": True,
        "message": "Payment method updated successfully"
    }


@router.get("/invoices", response_model=List[Invoice])
async def get_invoices():
    """Get invoice history"""
    # TODO: Implement actual invoice retrieval
    return [
        Invoice(
            id="INV-001",
            date="2024-07-15",
            amount="$99.00",
            status="paid",
            download_url="/invoices/INV-001.pdf"
        ),
        Invoice(
            id="INV-002",
            date="2024-06-15",
            amount="$99.00",
            status="paid",
            download_url="/invoices/INV-002.pdf"
        ),
    ]


@router.post("/api-keys", response_model=ApiKey)
async def create_api_key(request: ApiKeyCreate):
    """Create a new API key"""
    # TODO: Implement actual API key creation
    import secrets
    key = f"sk_live_{secrets.token_urlsafe(32)}"
    return ApiKey(
        id=str(len([]) + 1),
        name=request.name,
        key=key,
        created_at="2024-01-15",
        last_used=None
    )


@router.get("/api-keys", response_model=List[ApiKey])
async def get_api_keys():
    """Get all API keys"""
    # TODO: Implement actual API key retrieval
    return [
        ApiKey(
            id="1",
            name="Production API Key",
            key="sk_live_...abc123",
            created_at="2024-01-15",
            last_used="2 hours ago"
        ),
        ApiKey(
            id="2",
            name="Development API Key",
            key="sk_test_...xyz789",
            created_at="2024-06-01",
            last_used="1 week ago"
        ),
    ]


@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: str):
    """Delete an API key"""
    # TODO: Implement actual API key deletion
    return {
        "success": True,
        "message": f"API key {key_id} deleted successfully"
    }


@router.post("/webhooks", response_model=Webhook)
async def create_webhook(request: WebhookCreate):
    """Create a new webhook"""
    # TODO: Implement actual webhook creation
    return Webhook(
        id=str(len([]) + 1),
        url=request.url,
        events=request.events,
        status="active",
        created_at="2024-07-01"
    )


@router.get("/webhooks", response_model=List[Webhook])
async def get_webhooks():
    """Get all webhooks"""
    # TODO: Implement actual webhook retrieval
    return [
        Webhook(
            id="1",
            url="https://example.com/webhook",
            events=["call.completed", "agent.status_changed"],
            status="active",
            created_at="2024-07-01"
        ),
        Webhook(
            id="2",
            url="https://app.example.com/hooks",
            events=["call.started"],
            status="inactive",
            created_at="2024-06-15"
        ),
    ]


@router.put("/webhooks/{webhook_id}", response_model=Webhook)
async def update_webhook(webhook_id: str, request: WebhookUpdate):
    """Update a webhook"""
    # TODO: Implement actual webhook update
    return {
        "success": True,
        "message": f"Webhook {webhook_id} updated successfully",
        **request.model_dump(exclude_unset=True)
    }


@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: str):
    """Delete a webhook"""
    # TODO: Implement actual webhook deletion
    return {
        "success": True,
        "message": f"Webhook {webhook_id} deleted successfully"
    }


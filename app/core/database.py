"""
In-memory database storage (temporary until real database is implemented)
"""
from typing import List, Dict, Any
from app.schemas.agent import VoiceAgent
from app.schemas.call import Call
from app.schemas.contact import Contact

# Shared in-memory storage
agents_db: List[VoiceAgent] = []
calls_db: List[Call] = []
contacts_db: List[Contact] = []


def init_sample_data():
    """Initialize with sample data"""
    global agents_db, calls_db, contacts_db
    
    if not agents_db:
        agents_db.extend([
            VoiceAgent(
                id="1",
                name="Support Bot",
                description="Handles customer support inquiries",
                status="active",
                calls=120,
                avg_duration="4:32"
            ),
            VoiceAgent(
                id="2",
                name="Sales Bot",
                description="Handles sales inquiries and lead qualification",
                status="active",
                calls=95,
                avg_duration="5:15"
            ),
        ])
    
    if not contacts_db:
        contacts_db.extend([
            Contact(
                id="1",
                name="John Doe",
                email="john.doe@example.com",
                phone="+1 (555) 123-4567",
                company="Acme Corp",
                status="active",
                total_calls=5,
                last_contact="2024-01-15"
            ),
            Contact(
                id="2",
                name="Jane Smith",
                email="jane.smith@example.com",
                phone="+1 (555) 987-6543",
                company="Tech Inc",
                status="lead",
                total_calls=2,
                last_contact="2024-01-14"
            ),
        ])
    
    if not calls_db:
        calls_db.extend([
            Call(
                id="1",
                contact="John Doe",
                phone="+1 (555) 123-4567",
                agent="Support Bot",
                agent_id="1",
                type="inbound",
                duration="4:32",
                date="2024-01-15",
                time="14:30",
                status="completed",
                recording=True,
                outcome="success"
            ),
            Call(
                id="2",
                contact="Jane Smith",
                phone="+1 (555) 987-6543",
                agent="Sales Bot",
                agent_id="2",
                type="outbound",
                duration="5:15",
                date="2024-01-15",
                time="15:45",
                status="completed",
                recording=True,
                outcome="success"
            ),
        ])


"""
Database initialization script
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import init_db, AsyncSessionLocal
from app.models.agent import VoiceAgent, AgentStatus
from app.models.contact import Contact, ContactStatus
from app.models.call import Call, CallType, CallStatus, CallOutcome
from datetime import date, time


async def init_sample_data():
    """Initialize database with sample data"""
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        from sqlalchemy import select, func
        agent_count = await session.execute(select(func.count(VoiceAgent.id)))
        if agent_count.scalar() > 0:
            print("Sample data already exists. Skipping initialization.")
            return
        
        # Create sample agents
        agent1 = VoiceAgent(
            id="1",
            name="Support Bot",
            description="Handles customer support inquiries",
            status=AgentStatus.ACTIVE,
            calls_count=120,
            avg_duration="4:32"
        )
        
        agent2 = VoiceAgent(
            id="2",
            name="Sales Bot",
            description="Handles sales inquiries and lead qualification",
            status=AgentStatus.ACTIVE,
            calls_count=95,
            avg_duration="5:15"
        )
        
        session.add(agent1)
        session.add(agent2)
        await session.flush()
        
        # Create sample contacts
        contact1 = Contact(
            id="1",
            name="John Doe",
            email="john.doe@example.com",
            phone="+1 (555) 123-4567",
            company="Acme Corp",
            status=ContactStatus.ACTIVE,
            total_calls=5,
            last_contact=date(2024, 1, 15)
        )
        
        contact2 = Contact(
            id="2",
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1 (555) 987-6543",
            company="Tech Inc",
            status=ContactStatus.LEAD,
            total_calls=2,
            last_contact=date(2024, 1, 14)
        )
        
        session.add(contact1)
        session.add(contact2)
        await session.flush()
        
        # Create sample calls
        call1 = Call(
            id="1",
            contact_id=contact1.id,
            agent_id=agent1.id,
            contact_name="John Doe",
            phone="+1 (555) 123-4567",
            agent_name="Support Bot",
            type=CallType.INBOUND,
            duration="4:32",
            date=date(2024, 1, 15),
            time=time(14, 30),
            status=CallStatus.COMPLETED,
            recording=True,
            outcome=CallOutcome.SUCCESS
        )
        
        call2 = Call(
            id="2",
            contact_id=contact2.id,
            agent_id=agent2.id,
            contact_name="Jane Smith",
            phone="+1 (555) 987-6543",
            agent_name="Sales Bot",
            type=CallType.OUTBOUND,
            duration="5:15",
            date=date(2024, 1, 15),
            time=time(15, 45),
            status=CallStatus.COMPLETED,
            recording=True,
            outcome=CallOutcome.SUCCESS
        )
        
        session.add(call1)
        session.add(call2)
        
        await session.commit()
        print("Sample data initialized successfully!")


async def main():
    """Main initialization function"""
    print("Initializing database...")
    await init_db()
    print("Database tables created!")
    
    print("Initializing sample data...")
    await init_sample_data()


if __name__ == "__main__":
    asyncio.run(main())


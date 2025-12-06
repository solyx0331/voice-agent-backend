# Supabase Setup Guide

This guide will help you connect your backend to Supabase as your online PostgreSQL database.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Fill in your project details:
   - **Name**: Your project name (e.g., "Voice AI Agent")
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the closest region to your users
4. Click "Create new project"
5. Wait 2-3 minutes for the database to be provisioned

## Step 2: Get Your Connection String

1. In your Supabase project dashboard, go to **Settings** (gear icon)
2. Click on **Database** in the left sidebar
3. Scroll down to the **Connection string** section
4. Select the **URI** tab
5. Copy the connection string - it will look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```

## Step 3: Update Your .env File

1. Open your `.env` file in the Backend directory
2. Update the `DATABASE_URL` with your Supabase connection string
3. **Important**: You can use either `postgresql://` or `postgresql+psycopg://` - the code will automatically convert it

**Example:**
```env
DATABASE_URL=postgresql://postgres:your_password_here@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**Note**: 
- Replace `your_password_here` with your actual database password
- Replace `db.abcdefghijklmnop.supabase.co` with your actual project reference
- **Special characters in password**: If your password contains special characters like `@`, `$`, `#`, etc., they will be automatically URL-encoded by the application. You can paste the connection string directly from Supabase.

## Step 4: Run Database Migrations

Once your `.env` is configured, run the migrations to create your tables:

```bash
# Create initial migration (if not already done)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations to Supabase
alembic upgrade head
```

## Step 5: Initialize Sample Data (Optional)

```bash
python -m app.db.init_db
```

## Step 6: Test the Connection

Start your server:

```bash
python run.py
```

If everything is configured correctly, the server should start without database connection errors.

## Security Best Practices

1. **Never commit your `.env` file** - It's already in `.gitignore`
2. **Use environment variables** in production instead of `.env` files
3. **Enable Row Level Security (RLS)** in Supabase for production
4. **Use connection pooling** - Supabase provides connection pooler URLs (port 6543) for better performance

## Connection Pooling (Optional)

For better performance with multiple connections, Supabase provides a connection pooler:

1. In Supabase Dashboard → Settings → Database
2. Find the **Connection pooling** section
3. Use the **Session mode** connection string
4. Change the port from `5432` to `6543`
5. Update your `DATABASE_URL` accordingly

**Example with connection pooling:**
```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@db.abcdefghijklmnop.supabase.co:6543/postgres?pgbouncer=true
```

## Troubleshooting

### Connection Timeout
- Check your internet connection
- Verify the connection string is correct
- Ensure your IP is not blocked (check Supabase dashboard)

### Authentication Failed
- Double-check your database password
- Make sure you're using the correct project reference
- Verify the connection string format

### SSL Required
Supabase requires SSL connections. The `psycopg` driver handles this automatically, but if you encounter SSL errors, you can explicitly enable it:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@host:5432/postgres?sslmode=require
```

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase PostgreSQL Guide](https://supabase.com/docs/guides/database)
- [Connection Pooling Guide](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)


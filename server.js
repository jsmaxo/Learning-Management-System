const express = require('express');
const path = require('path');
const { Client } = require('pg');

const app = express();

// ✅ PostgreSQL connection settings
const con = new Client({
    host: "localhost",     // if Node goes into Docker and Postgres is also in Docker network, change to the Postgres container name
    user: "postgres",
    port: 5432,
    password: "admin",
    database: "sampledb"
});

con.connect()
    .then(() => console.log("✅ Connected to PostgreSQL"))
    .catch(err => console.error("❌ Connection error:", err.message));

// ✅ Serve static files (images, css, js, etc.)
app.use('/static', express.static(path.join(__dirname, 'static')));

// ✅ Serve the admin students dashboard page
// http://localhost:3000/admin_students
app.get('/admin_students', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'admin_students.html'));
});

// ✅ API endpoint to fetch student data as JSON
// http://localhost:3000/api/students
app.get('/api/students', async (req, res) => {
    try {
        // adjust column names based on your table definition
        const result = await con.query(`
            SELECT id,
                   first_name,
                   address1,
                   nic,
                   mobile,
                   district
            FROM students
            ORDER BY id ASC;
        `);

        res.json(result.rows);
    } catch (err) {
        console.error("❌ Query error:", err.message);
        res.status(500).json({ error: 'Database query failed' });
    }
});

// ✅ Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
    console.log(`👉 Open http://localhost:${PORT}/admin_students`);
});

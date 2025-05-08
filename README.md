# IPL Data Analysis System

This is a comprehensive application for analyzing Indian Premier League (IPL) data. The system consists of a React/Next.js frontend and a Flask backend API that connects to a MySQL database to provide player statistics, team information, auction data, and analytical tools.

## Features

- **User Authentication**: Different access levels for normal users and team owners
- **Player Statistics**: Comprehensive batting and bowling statistics for all IPL players
- **Team Management**: Team composition analysis and player management tools
- **Player Comparison**: Side-by-side comparison of player statistics
- **Auction Strategy**: Tools for team owners to plan auction strategies
- **Player Valuation**: Advanced metrics for player valuation and team building

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.6 or higher)
- MySQL database (v5.7 or higher)
- npm or yarn package manager

## Project Structure

\`\`\`
ipl-data-analysis/
├── app/                    # Next.js app directory
│   ├── dashboard/          # Dashboard pages
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Home/login page
├── components/             # React components
│   ├── ui/                 # UI components (shadcn/ui)
│   ├── dashboard-header.tsx
│   ├── login-form.tsx
│   ├── player-comparison.tsx
│   ├── player-stats.tsx
│   ├── team-owner-panel.tsx
│   └── ...
├── lib/                    # Utility functions
│   ├── api.ts              # API client functions
│   └── utils.ts            # Helper utilities
├── public/                 # Static assets
├── app.py                  # Flask backend application
├── package.json            # Frontend dependencies
└── README.md               # Project documentation
\`\`\`

## Setup Instructions

### Database Setup

1. Create a MySQL database:
   \`\`\`sql
   CREATE DATABASE dbms_proj;
   \`\`\`

2. Import the database schema (if you have a SQL dump file):
   \`\`\`bash
   mysql -u username -p dbms_proj < schema.sql
   \`\`\`

3. Alternatively, set up the required tables manually:
   \`\`\`sql
   CREATE TABLE Player (
     player_id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(100) NOT NULL,
     nationality VARCHAR(50),
     playing_role VARCHAR(50),
     batting_style VARCHAR(50),
     bowling_style VARCHAR(50),
     current_market_price DECIMAL(10,2),
     base_bid DECIMAL(10,2),
     dob DATE
   );

   CREATE TABLE Team (
     team_id INT AUTO_INCREMENT PRIMARY KEY,
     team_name VARCHAR(100) NOT NULL,
     home_ground VARCHAR(100),
     points_ranking INT
   );

   CREATE TABLE Batting_Stats (
     player_id INT PRIMARY KEY,
     matches INT,
     runs INT,
     average DECIMAL(6,2),
     strike_rate DECIMAL(6,2),
     half_century INT,
     century INT,
     FOREIGN KEY (player_id) REFERENCES Player(player_id)
   );

   CREATE TABLE Bowling_Stats (
     player_id INT PRIMARY KEY,
     matches INT,
     wickets INT,
     average DECIMAL(6,2),
     economy DECIMAL(6,2),
     strike_rate DECIMAL(6,2),
     FOREIGN KEY (player_id) REFERENCES Player(player_id)
   );

   CREATE TABLE Auction_History (
     auction_id INT AUTO_INCREMENT PRIMARY KEY,
     player_id INT,
     year INT,
     sold_price VARCHAR(20),
     base_price VARCHAR(20),
     bidding_teams TEXT,
     FOREIGN KEY (player_id) REFERENCES Player(player_id)
   );
   \`\`\`

### Backend Setup

1. Create a Python virtual environment:
   \`\`\`bash
   python -m venv venv
   \`\`\`

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install required Python packages:
   \`\`\`bash
   pip install flask flask-cors mysql-connector-python
   \`\`\`

4. Configure the database connection in `app.py`:
   \`\`\`python
   DB_CONFIG = {
       "host": "localhost",
       "user": "your_username",
       "password": "your_password",
       "database": "dbms_proj",
   }
   \`\`\`

5. Start the Flask backend:
   \`\`\`bash
   python app.py
   \`\`\`
   The API will be available at http://127.0.0.1:5000

### Frontend Setup

1. Install Node.js dependencies:
   \`\`\`bash
   npm install
   # or
   yarn install
   \`\`\`

2. Configure the API URL in your environment:
   - Create a `.env.local` file in the project root:
     \`\`\`
     NEXT_PUBLIC_API_URL=http://127.0.0.1:5000
     \`\`\`

3. Start the development server:
   \`\`\`bash
   npm run dev
   # or
   yarn dev
   \`\`\`

4. Open your browser and navigate to http://localhost:3000

## API Endpoints

The backend provides the following API endpoints:

### Players

- `GET /api/players` - Get all players
- `POST /api/players/add` - Add a new player
- `GET /api/players/batting/:player_id` - Get batting statistics for a player
- `GET /api/players/bowling/:player_id` - Get bowling statistics for a player
- `GET /api/players/auction/:player_id` - Get auction history for a player

### Teams

- `GET /api/teams` - Get all teams
- `GET /api/team/:team_id/full` - Get team details with players

## Technologies Used

### Frontend
- Next.js 14 (React framework)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Lucide React icons

### Backend
- Flask (Python web framework)
- MySQL Connector/Python
- Flask-CORS

### Database
- MySQL

## Troubleshooting

### API Connection Issues

If you encounter API connection issues:

1. Ensure the Flask backend is running
2. Check that the `NEXT_PUBLIC_API_URL` environment variable is set correctly
3. Verify that CORS is properly configured in the Flask app
4. Check the browser console for specific error messages

### Database Connection Issues

If the backend cannot connect to the database:

1. Verify MySQL is running
2. Check the database credentials in `app.py`
3. Ensure the database and tables exist
4. Check MySQL user permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

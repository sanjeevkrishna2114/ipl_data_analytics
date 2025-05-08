import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# MySQL Database Configuration (Use environment variables in production)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sky36@21",
    "database": "dbms_proj",
}

# Function to execute MySQL queries safely
def query_db(query, args=(), one=False):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
   
    cursor.close()  # Properly close the cursor
    conn.close()  # Properly close the connection

    return (result[0] if result else None) if one else result

# Function to execute MySQL insert/update queries
def execute_db(query, args=()):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise e

# Route to get all players
@app.route("/api/players")
def get_players():
    data = query_db("SELECT player_id, name, nationality, playing_role, batting_style, bowling_style, current_market_price, base_bid, dob FROM Player")
   
    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "nationality": row[2],  
            "role": row[3],
            "battingStyle": row[4],
            "bowlingStyle": row[5],
            "marketPrice": row[6],
            "baseBid": row[7],
            "dob": str(row[8])  # Convert DATE to string for JSON serialization
        } for row in data
    ])

# Route to add a new target player
@app.route("/api/players/add", methods=["POST"])
def add_player():
    data = request.json
    
    # Validate required fields
    required_fields = ["name", "nationality", "role", "baseBid"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        # Insert the new player into the Player table
        query = """
        INSERT INTO Player (name, nationality, playing_role, base_bid) 
        VALUES (%s, %s, %s, %s)
        """
        
        player_id = execute_db(
            query, 
            (data["name"], data["nationality"], data["role"], data["baseBid"])
        )
        
        return jsonify({
            "success": True,
            "message": "Player added successfully",
            "player_id": player_id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get batting stats
@app.route("/api/players/batting/<int:player_id>")
def get_batting(player_id):
    row = query_db("SELECT matches, runs, average, strike_rate, half_century, century FROM Batting_Stats WHERE player_id=%s", (player_id,), one=True)
   
    if row is None:
        return jsonify({"error": "Player not found"}), 404  
   
    return jsonify({
        "matches": row[0],
        "runs": row[1],
        "average": row[2],
        "strikeRate": row[3],
        "fifties": row[4],
        "hundreds": row[5]
    })

# Route to get bowling stats
@app.route("/api/players/bowling/<int:player_id>")
def get_bowling(player_id):
    row = query_db("SELECT matches, wickets, average, economy, strike_rate FROM Bowling_Stats WHERE player_id=%s", (player_id,), one=True)
   
    if row is None:
        return jsonify({"error": "Player not found"}), 404  
   
    return jsonify({
        "matches": row[0],
        "wickets": row[1],
        "average": row[2],
        "economy": row[3],
        "strikeRate": row[4]
    })

# Route to get auction history
@app.route("/api/players/auction/<int:player_id>")
def get_auction(player_id):
    rows = query_db("SELECT year, sold_price, base_price, bidding_teams FROM Auction_History WHERE player_id=%s", (player_id,))
   
    if not rows:
        return jsonify({"message": "No auction history found"}), 404
   
    return jsonify([
        {"year": row[0], "soldPrice": row[1], "basePrice": row[2], "biddingTeams": row[3]} for row in rows
    ])

# Route to get all teams
@app.route("/api/teams")
def get_teams():
    data = query_db("SELECT team_id, team_name, home_ground, points_ranking FROM Team")
    return jsonify([
        {
            "team_id": row[0],
            "team_name": row[1],
            "home_ground": row[2],
            "points_ranking": row[3]
        }
        for row in data
    ])

@app.route("/")
def home():
    return "🚀 IPL API is up!"

if __name__ == "__main__":
    app.run(debug=True)

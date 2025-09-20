from flask import Flask, request, jsonify
from models import data_base, Game, Player


def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    data_base.init_app(app)
    


#Player
    @app.route('/api/players', methods=['GET'])
    def get_players():
        try:
            players = Player.query.all()
            return jsonify([player.to_dict(include_games=False) for player in players]), 200
        except Exception as e:
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/players/<int:id>', methods=['GET'])
    def get_player(id):
        try:
            player = Player.query.get_or_404(id)
            return jsonify(player.to_dict(include_games=True)), 200
        except Exception as e:
            if "404" in str(e):
                return jsonify({"error": "Player not found"}), 404
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/players', methods=['POST'])
    def create_player():
        try:
            data = request.get_json()
            player = Player(
                username=data['username']
            )
            data_base.session.add(player)
            data_base.session.commit()
            return jsonify(player.to_dict()), 201
        except Exception as e:
            data_base.session.rollback()
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/players/<int:id>', methods=['PATCH'])
    def update_player(id):
        try:
            player = Player.query.get_or_404(id)
            data = request.get_json()
            
            if 'username' in data:
                player.username = data['username']
            
            data_base.session.commit()
            return jsonify(player.to_dict(include_games=True)), 200
        except Exception as e:
            data_base.session.rollback()
            if "404" in str(e):
                return jsonify({"error": "Player not found"}), 404
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/players/<int:id>', methods=['DELETE'])
    def delete_player(id):
        try:
            player = Player.query.get_or_404(id)
            data_base.session.delete(player)
            data_base.session.commit()
            return '', 202
        except Exception as e:
            data_base.session.rollback()
            if "404" in str(e):
                return jsonify({"error": "Player not found"}), 404
            return jsonify({"status": 500, "reason": str(e)}), 500



#Games
    @app.route('/api/games', methods=['GET'])
    def get_games():
        try:
            games = Game.query.all()
            return jsonify([game.to_dict() for game in games]), 200
        except Exception as e:
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/games/<int:id>', methods=['GET'])
    def get_game(id):
        try:
            game = Game.query.get_or_404(id)
            return jsonify(game.to_dict()), 200
        except Exception as e:
            if "404" in str(e):
                return jsonify({"error": "Game not found"}), 404
            return jsonify({"status": 500, "reason": str(e)}), 500

    @app.route('/api/games', methods=['POST'])
    def create_game():
        try:
            data = request.get_json()
            game = Game(
                title=data['title'],
                price=data.get('price', 0.0),
                release_year=data.get('release_year'),
                weight=data.get('weight'),
                genre=data.get('genre'),
                player_id=data['player_id']
            )
            data_base.session.add(game)
            data_base.session.commit()
            return jsonify(game.to_dict()), 201
        except Exception as e:
            data_base.session.rollback()
            return jsonify({"status": 500, "reason": str(e)}), 500

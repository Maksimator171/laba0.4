from flask_sqlalchemy import SQLAlchemy

data_base = SQLAlchemy()

class Player(data_base.Model):
    __tablename__ = "players"

    id = data_base.Column(data_base.Integer, primary_key=True)
    username = data_base.Column(data_base.String(100), nullable=False, unique=True)
    
    games = data_base.relationship('Game', backref='player', lazy=True)

    def to_dict(self, include_games=False):
        result = {
            'id': self.id,
            'username': self.username,
        }
        
        if include_games:
            result['games'] = [game.to_dict() for game in self.games]
            
        return result


class Game(data_base.Model):
    __tablename__ = "games"

    id = data_base.Column(data_base.Integer, primary_key=True)
    title = data_base.Column(data_base.String(200), nullable=False)
    price = data_base.Column(data_base.Float, default=0.0) 
    release_year = data_base.Column(data_base.Integer) 
    weight = data_base.Column(data_base.Float) 
    genre = data_base.Column(data_base.String(100))
    
    player_id = data_base.Column(data_base.Integer, data_base.ForeignKey('players.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'release_year': self.release_year,
            'weight': self.weight,
            'genre': self.genre,
            'player_id': self.player_id
        }

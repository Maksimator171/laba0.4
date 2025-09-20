import pytest
import json
from main import app, data_base
from models import Player, Game

def setup_database():
    with app.app_context():
        data_base.drop_all()
        data_base.create_all()

def cleanup_database():
    with app.app_context():
        data_base.drop_all()

#Tests for Player
class TestPlayer:
    def setup_method(self):
        setup_database()
        with app.app_context():
            base_player = Player(username="test_player")
            data_base.session.add(base_player)
            data_base.session.commit()

    def teardown_method(self):
        cleanup_database()

    def test_get_players(self):
        with app.test_client() as client:
            response = client.get('/api/players')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['username'] == "test_player"

    def test_get_player_by_id(self):
        with app.test_client() as client:
            response = client.get('/api/players/1')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['username'] == "test_player"
            assert data['id'] == 1

    def test_create_player(self):
        with app.test_client() as client:
            new_player = {'username': 'new_player'}
            response = client.post('/api/players', json=new_player, content_type='application/json')
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['username'] == 'new_player'
            
            response = client.get('/api/players')
            data = json.loads(response.data)
            assert len(data) == 2

    def test_create_duplicate_player(self):
        with app.test_client() as client:
            duplicate_player = {'username': 'test_player'}
            response = client.post('/api/players', json=duplicate_player, content_type='application/json')
            assert response.status_code == 500

    def test_update_player(self):
        with app.test_client() as client:
            update_data = {'username': 'updated_player'}
            response = client.patch('/api/players/1', json=update_data, content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['username'] == 'updated_player'
            
            response = client.get('/api/players/1')
            data = json.loads(response.data)
            assert data['username'] == 'updated_player'

    def test_delete_player(self):
        with app.test_client() as client:
            response = client.get('/api/players/1')
            assert response.status_code == 200
            
            response = client.delete('/api/players/1')
            assert response.status_code == 202
            
            response = client.get('/api/players/1')
            assert response.status_code == 404

    def test_delete_nonexistent_player(self):
        with app.test_client() as client:
            response = client.delete('/api/players/999')
            assert response.status_code == 404

# Tests for Game
class TestGame:
    def setup_method(self):
        setup_database()
        with app.app_context():
            base_player = Player(username="test_player")
            data_base.session.add(base_player)
            
            base_game = Game(
                title="Test Game",
                price=49.99,
                release_year=2023,
                weight=150.0,
                genre="Action",
                player_id=1
            )
            data_base.session.add(base_game)
            data_base.session.commit()

    def teardown_method(self):
        cleanup_database()


    def test_get_games(self):
        with app.test_client() as client:
            response = client.get('/api/games')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['title'] == "Test Game"
            assert data[0]['price'] == 49.99

    def test_get_game_by_id(self):
        with app.test_client() as client:
            response = client.get('/api/games/1')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['title'] == "Test Game"
            assert data['release_year'] == 2023
            assert data['player_id'] == 1

    def test_create_game(self):
        with app.test_client() as client:
            new_game = {
                'title': 'New Game',
                'price': 29.99,
                'release_year': 2024,
                'weight': 120.0,
                'genre': 'RPG',
                'player_id': 1
            }
            response = client.post('/api/games', json=new_game, content_type='application/json')
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['title'] == 'New Game'
            assert data['genre'] == 'RPG'
            
            response = client.get('/api/games')
            data = json.loads(response.data)
            assert len(data) == 2

    def test_create_game_without_required_fields(self):
        with app.test_client() as client:
            incomplete_game = {
                'price': 29.99,
                'release_year': 2024
            }
            response = client.post('/api/games', json=incomplete_game, content_type='application/json')
            assert response.status_code == 500

    def test_update_game(self):
        with app.test_client() as client:
            update_data = {
                'title': 'Updated Game',
                'price': 39.99,
                'genre': 'Adventure'
            }
            response = client.patch('/api/games/1', json=update_data, content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['title'] == 'Updated Game'
            assert data['price'] == 39.99
            assert data['genre'] == 'Adventure'
            assert data['release_year'] == 2023

    def test_delete_game(self):
        with app.test_client() as client:
            response = client.get('/api/games/1')
            assert response.status_code == 200
            
            response = client.delete('/api/games/1')
            assert response.status_code == 202
            
            response = client.get('/api/games/1')
            assert response.status_code == 404

    def test_delete_nonexistent_game(self):
        with app.test_client() as client:
            response = client.delete('/api/games/999')
            assert response.status_code == 404

    def test_get_player_with_games(self):
        with app.test_client() as client:
            response = client.get('/api/players/1')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'games' in data
            assert len(data['games']) == 1
            assert data['games'][0]['title'] == "Test Game"

    def test_create_game_for_nonexistent_player(self):
        with app.test_client() as client:
            new_game = {
                'title': 'New Game',
                'price': 29.99,
                'player_id': 999
            }
            response = client.post('/api/games', json=new_game, content_type='application/json')
            assert response.status_code == 500

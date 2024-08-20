import pytest
from app import app
import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown(client):
    """
    Setup: Ensure that the habits table is cleared before each test.
    Teardown: Clear the habits table after each test to maintain isolation.
    """
    # Clear habits table before each test
    client.post('/clear_habits_table')
    yield
    # Clear habits table after each test
    client.post('/clear_habits_table')

def test_habit_creation(client):
    """
    Test the creation of a new habit.
    """    
    response = client.post('/habits', json={
        'name': 'Test Habit',
        'periodicity': 'D'
    })
    assert response.json == {'message': 'Habit created successfully'}
    # check if it's in the database
    response = client.get('/habits/Test Habit')
    assert len(response.json) != 0

def test_habit_deletion(client):
    """
    Test the deletion of a habit.
    """
    response = client.post('/habits', json={
        'name': 'Test Habit',
        'periodicity': 'D'
    })
    assert response.status_code == 200

    response = client.delete('/habits/Test Habit')
    assert response.status_code == 200
    assert response.json == {'message': 'Habit Test Habit deleted successfully'}
    # check if it's not in the database
    response = client.get('/habits/Test Habit')
    # assert response is empty, no data returned
    assert response.json == None 

def test_habit_completion(client):
    """
    Test the completion of a habit.
    """    
    response = client.post('/habits', json={
        'name': 'Test Habit',
        'periodicity': 'D'
    })
    assert response.status_code == 200
    response = client.put('/habits/Test Habit')
    assert response.status_code == 200
    assert response.json == {'message': 'Habit Test Habit marked as completed'}
    # check if it's in the database
    response = client.get('/habits/Test Habit')
    assert response.status_code == 200
    # assert streak value is 1
    assert response.json[4] == 1

def test_habit_already_exists(client):
    """
    Test that a habit cannot be created if it already exists.
    """    
    response = client.post('/habits', json={
        'name': 'Test Habit',
        'periodicity': 'D'
    })
    assert response.status_code == 200
    response = client.post('/habits', json={
        'name': 'Test Habit',
        'periodicity': 'D'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Habit already exists'}

def test_habit_name_empty(client):
    """
    Test that a habit cannot be created if the name is empty.
    """
    response = client.post('/habits', json={
        'name': '',
        'periodicity': 'D'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Habit name cannot be empty'}


def test_create_initial_habits(client):
    """
    Test that the default habits in the JSON file are actually created
    """
    # get names of habits from JSON file
    names_of_habits = []
    with open('./test_data/predefined_habits.json') as f:
        data = json.load(f)
        for habit in data:
            names_of_habits.append(habit['name'])
    response = client.post('/create_initial_habits')
    assert response.status_code == 200
    assert response.json == {'status': 'success'}
    response = client.get('/habits')
    assert response.status_code == 200
    # make sure all of names_of_habits are in the response
    for habit in response.json:
        assert habit[1] in names_of_habits

def test_clear_habits_table(client):
    """
    Test that the habits table can be cleared.
    """
    response = client.post('/clear_habits_table')
    assert response.status_code == 200
    assert response.json == {'status': 'success'}
    # assert that the table is actually empty
    response = client.get('/habits')
    assert response.status_code == 200
    assert len(response.json) == 0

def test_habit_tracking_data_dimensions(client):
    """
    Test that the habit tracking data has the correct dimensions.
    """
    # create initial habits for testing
    response = client.post('/create_initial_habits')
    assert response.status_code == 200
    assert response.json == {'status': 'success'}
    response = client.get('/habits')
    assert response.status_code == 200
    habit_id = response.json[0][0] # get first habit's name
    response = client.get(f'/habits/tracking/{habit_id}')
    assert response.status_code == 200
    # assert that the response only has 0 or 1 values
    for list_of_values in response.json.values():
        for value in list_of_values:
            assert value == 0 or value == 1
    # assert that each year has length of 365 or 366, if it's a leap year, no matter the periodicity
    for key in response.json.keys():
        assert len(response.json[key]) == 365 or len(response.json[key]) == 366

if __name__ == '__main__':
    pytest.main()

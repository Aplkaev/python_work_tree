from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

json_trees = {
    'parent': {
        "name": "test 1",
        "tree_id": 0,
        "start_date": "2024-05-21T11:04:23.452000",
        "end_date": "2024-05-21T11:04:23.452000"
    },
    'children_1': {
        "name": "test 2",
        "tree_id": 0,
        "start_date": "2024-01-21T11:04:23.452000",
        "end_date": "2024-09-21T11:04:23.452000"
    },
    'children_2': {
        "name": "test 3",
        "tree_id": 0,
        "start_date": "2024-01-21T11:04:23.452000",
        "end_date": "2024-12-21T11:04:23.452000",
        "parent_id": ''
    },
    'children_3': {
        "name": "test 4",
        "tree_id": 0,
        "start_date": "2023-02-21T11:04:23.452000",
        "end_date": "2024-10-21T11:04:23.452000",
        "parent_id": ''
    }
}


def test_add_one_work():
    name = 'test_add_one_work'
    response = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json={
            "name": name,
            "tree_id": 2,
            "start_date": "2024-05-21T11:04:23.452Z",
            "end_date": "2024-05-21T11:04:23.452Z"
        },
    )
    assert response.status_code == 200
    assert response.json()['name'] == name


def test_add_works():
    # первая работа
    response_parent = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['parent'],
    )
    assert response_parent.status_code == 200

    json_trees['children_1']['parent_id'] = response_parent.json()['id']
    json_trees['children_2']['parent_id'] = response_parent.json()['id']
    # вторая работа дочернаяя
    response_children_1 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_1'],
    )
    assert response_children_1.status_code == 200

    # третья работа дочернаяя
    response_children_2 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_2'],
    )
    assert response_children_2.status_code == 200

    json_trees['children_3']['parent_id'] = response_children_1.json()['id']
    # четвертая работа дочернаяя
    response_children_3 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_3'],
    )
    assert response_children_3.status_code == 200

    # получам родителя и проверям время=
    response_parent_1_update = client.get(
        "/work/" + response_parent.json()['id'],
        headers={"X-Token": "coneofsilence"},
    )
    assert response_parent_1_update.status_code == 200
    assert response_parent_1_update.json()['start_date'] \
        == json_trees['children_3']['start_date']
    assert response_parent_1_update.json()['end_date'] \
        == json_trees['children_3']['end_date']


def test_update_works():
    # первая работа
    response_parent = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['parent'],
    )
    assert response_parent.status_code == 200

    json_trees['children_1']['parent_id'] = response_parent.json()['id']
    json_trees['children_2']['parent_id'] = response_parent.json()['id']
    # вторая работа дочернаяя
    response_children_1 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_1'],
    )
    assert response_children_1.status_code == 200

    # третья работа дочернаяя
    response_children_2 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_2'],
    )
    assert response_children_2.status_code == 200

    json_trees['children_3']['parent_id'] = response_children_1.json()['id']
    # четвертая работа дочернаяя
    response_children_3 = client.post(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_3'],
    )
    assert response_children_3.status_code == 200

    json_trees['children_3']['id'] = response_children_3.json()['id']
    json_trees['children_3']['end_date'] = "2026-10-21T11:04:23.452000"
    # четвертая работа дочернаяя
    response_children_3 = client.put(
        "/work",
        headers={"X-Token": "coneofsilence"},
        json=json_trees['children_3'],
    )
    assert response_children_3.status_code == 200

    # получам родителя и проверям время=
    response_parent_1_update = client.get(
        "/work/" + json_trees['children_1']['parent_id'],
        headers={"X-Token": "coneofsilence"},
    )
    assert response_parent_1_update.status_code == 200
    assert response_parent_1_update.json()['start_date'] \
        == json_trees['children_3']['start_date']
    assert response_parent_1_update.json()['end_date'] \
        == json_trees['children_3']['end_date']


def test_get_all():
    response = client.get(
        "/work?skip=0&limit=100",
        headers={"X-Token": "coneofsilence"},
    )
    assert response.status_code == 200

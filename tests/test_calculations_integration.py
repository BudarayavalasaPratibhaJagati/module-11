def test_calculation_crud_flow(client):
    # Create
    create_payload = {"expression": "1+1", "result": 2.0}
    r_create = client.post("/calculations", json=create_payload)
    assert r_create.status_code == 201
    created = r_create.json()
    calc_id = created["id"]

    # Browse
    r_list = client.get("/calculations")
    assert r_list.status_code == 200
    all_calcs = r_list.json()
    assert any(c["id"] == calc_id for c in all_calcs)

    # Read
    r_read = client.get(f"/calculations/{calc_id}")
    assert r_read.status_code == 200
    assert r_read.json()["id"] == calc_id

    # Edit
    update_payload = {"expression": "2+2", "result": 4.0}
    r_update = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert r_update.status_code == 200
    assert r_update.json()["expression"] == "2+2"

    # Delete
    r_delete = client.delete(f"/calculations/{calc_id}")
    assert r_delete.status_code == 204

    # Confirm gone
    r_missing = client.get(f"/calculations/{calc_id}")
    assert r_missing.status_code == 404


def test_invalid_calculation_payload(client):
    # Missing result field should give validation error
    r = client.post("/calculations", json={"expression": "1+1"})
    assert r.status_code == 422

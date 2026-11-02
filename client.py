import requests

url = "http://127.0.0.1:5000"
url_with_notes = "http://127.0.0.1:5000/notes"

r1 = requests.post(url_with_notes, json={"text": "Hello", "author": "Person1"})
r2 = requests.post(url_with_notes, json={"text": "Hi", "author": "Person2"})
r3 = requests.post(url_with_notes, json={"text": "Hello, i am 3", "author": "Person3"})
r4 = requests.post(url_with_notes, json={"text": "Hi, i am 4", "author": "Person4"})
r5 = requests.post(url_with_notes, json={"text": "Hello, i am 5", "author": "Person5"})
r6 = requests.post(url_with_notes, json={"text": "bye", "author": "Person5"})

for i in range(1, 5, 2):
    r = requests.post(f"{url_with_notes}/{i}/like")

r7 = requests.post(f"{url_with_notes}/3/like")
r8 = requests.post(f"{url_with_notes}/5/like")
r9 = requests.post(f"{url_with_notes}/5/like")

# POST /notes
r10 = requests.post(url_with_notes, json={"text": "Hi"})
print(f"r10){r10.status_code} - ожидается 400")
r11 = requests.post(url_with_notes, json={"author": "Person"})
print(f"r11){r11.status_code} - ожидается 400")

# PUT /notes/<id>
r12 = requests.put(f"{url_with_notes}/1", json={"author": "Person999", "text": "I am Person999"})
print(f"r12){r12.status_code} - ожидается 200")
r13 = requests.put(f"{url_with_notes}/999", json={"author": "Person999", "text": "I am Person999"})
print(f"r13){r13.status_code} - ожидается 404")
r14 = requests.put(f"{url_with_notes}/1", json={"author": 999, "text": "I am Person999"})
print(f"r14){r14.status_code} - ожидается 400")
r15 = requests.put(f"{url_with_notes}/1", json={"author": "Person000", "text": 0})
print(f"r15){r15.status_code} - ожидается 400")
r16 = requests.put(f"{url_with_notes}/1", json={"author": "Person000"})
print(f"r16){r16.status_code} - ожидается 400")
r17 = requests.put(f"{url_with_notes}/1", json={"text": 0})
print(f"r17){r17.status_code} - ожидается 400")

# GET /notes?author=<имя>&limit=<n>&offset=<m>
r18 = requests.get(f"{url_with_notes}?author=Person5")
print(f"r18){r18.status_code} - ожидается 200, ответ: {r18.json()}")
r19 = requests.get(f"{url_with_notes}?author=Person5&limit=y")
print(f"r19){r19.status_code} - ожидается 400")

# PATCH /notes/<id>
r20 = requests.patch(f"{url_with_notes}/1", json={"text": "Hello my friend"})
print(f"r20){r20.status_code} - ожидается 200")
r21 = requests.patch(f"{url_with_notes}/999", json={"text": "Hello my friend"})
print(f"r21){r21.status_code} - ожидается 404")
r22 = requests.patch(f"{url_with_notes}/1", json={"text": 50})
print(f"r22){r22.status_code} - ожидается 400")

# POST /notes/<id>/like
r23 = requests.post(f"{url_with_notes}/1/like")
print(f"r23){r23.status_code} - ожидается 200")
r24 = requests.post(f"{url_with_notes}/999/like")
print(f"r24){r24.status_code} - ожидается 404")

# GET /notes
r25 = requests.get(f"{url_with_notes}?sort=likes&order=desc")
print(f"r25){r25.status_code} - ожидается 200")
r26 = requests.get(f"{url_with_notes}?sort=authors&order=desc")
print(f"r26){r26.status_code} - ожидается 400")
r27 = requests.get(f"{url_with_notes}?sort=likes&order=aaa")
print(f"r27){r27.status_code} - ожидается 400")

# GET /authors
r28 = requests.get(f"{url}/authors")
print(f"r28){r28.status_code} - ожидается 200, ответ: {r28.json()}")

# DELETE /notes?author=<имя>
r29 = requests.delete(f"{url_with_notes}?author=Person5")
print(f"r29){r29.status_code} - ожидается 200, ответ: {r29.json()}")
r30 = requests.delete(f"{url_with_notes}")
print(f"r30){r30.status_code} - ожидается 400")
r31 = requests.delete(f"{url_with_notes}?author=999")
print(f"r31){r31.status_code} - ожидается 200, ответ: {r31.json()}")
r32 = requests.delete(f"{url_with_notes}?author=")
print(f"r32){r32.status_code} - ожидается 400")
r33 = requests.delete(f"{url_with_notes}?author=   ")
print(f"r33){r33.status_code} - ожидается 400")
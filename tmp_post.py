import requests, json
r = requests.post('http://127.0.0.1:5001/api/generate', json={
  'prompt': 'Gerar um cliente Python simples para GET https://httpbin.org/get com headers e timeout.',
  'name': 'teste-httpbin'
})
print(r.status_code)
print(r.text)

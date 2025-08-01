<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>STAY-Watcher Shrine</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="container">
    <h1>STAY-Watcher Shrine 🌙</h1>
    <p>Watching Stray Kids' Instagram lives:</p>
    <ul>
      {% for user in users %}
      <li>
        <strong>@{{ user }}</strong> –
        {% if statuses[user] %}<span class="live">🔴 LIVE</span>
        {% else %}<span class="offline">💤 Offline</span>{% endif %}
      </li>
      {% endfor %}
    </ul>
    <p class="note">Status updates every few minutes.</p>
  </div>
</body>
</html>

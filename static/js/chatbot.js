function sendMessage(event) {
  var input = document.getElementById('messageText');
  event.preventDefault();

  if (input.value) {
    var userMessage = document.createElement('li');
    userMessage.textContent = input.value;
    userMessage.className = 'user-message';
    document.getElementById('messages').appendChild(userMessage);

    const eventSource = new EventSource(
      'http://127.0.0.1:8080/chatbot/send?query=' + input.value
    );

    var agentMessage = document.createElement('li');
    const timestamp = new Date().toLocaleTimeString();
    agentMessage.id = timestamp;
    agentMessage.className = 'agent-message';
    agentMessage.textContent = 'Typing...';
    document.getElementById('messages').appendChild(agentMessage);

    eventSource.onopen = function () {
      console.log('Connection to chatbot established');
    };

    eventSource.onmessage = function (event) {
      try {
        const messageResponse = JSON.parse(event.data);
        if (messageResponse.response) {
          if (agentMessage.textContent === 'Typing...') {
            agentMessage.textContent = '';
          }
          const partOfMessage = messageResponse.response;
          agentMessage.textContent += partOfMessage;
        }
      } catch (error) {
        console.warn('Error occurred:', error);
      }
    };

    eventSource.onerror = function (error) {
      console.error('Error occurred:', error);
      eventSource.close();
    };

    input.value = '';
  } else {
    alert('Please enter a message');
  }
}

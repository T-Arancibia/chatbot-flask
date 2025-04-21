//Aqui se establecen los fetch hacia los endpoints de la api (routes.py)

//Se rescatan los id de las secciones de index.html que registran informacion importante para realizar los fetch al back-end

const loginSection = document.getElementById("pseudo-login");
const chatSection = document.getElementById("seccion-chat");
const usernameInput = document.getElementById("username");
const loginBtn = document.getElementById("login-button");
const historyList = document.getElementById("historial-chats");
const chatbox = document.getElementById("chat-box");
const form = document.getElementById("add-message");
const messageInput = document.getElementById("message");
const newConversationBtn = document.getElementById("nueva-conversacion");

let currentUserId = null;
let currentUsername = "";
let conversationId = null;


//Aca se muestran los mensajes visualmente, y dependiendo de quien lo envie, se muestra a la izquierda o a la derecha (y color grios o azul, respectivamente)
function appendMessage(role, content) {
  const msg = document.createElement("div");
  msg.className = `p-2 rounded ${
    role === "user" ? "bg-blue-100 text-right" : "bg-gray-200 text-left"
  }`;
  msg.innerText = content;
  chatbox.appendChild(msg);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function clearChat() {
  chatbox.innerHTML = "";
}

//Para acceder al historial, se debe hacer un fetch con el id del usuario, en donde se extraen la conversaciones de dicho usuario
async function loadConversations(userId) {
  const res = await fetch(`/history/${userId}`);
  return await res.json();
}
//Logica muy similar a la de acceso al historial de conversaciones, solo que en este caso de extraen los mensajes de una conversacion en especifico
async function loadMessages(conversationId) {
  const res = await fetch(`/conversation/${conversationId}`);
  const messages = await res.json();
  clearChat();
  messages.forEach((msg) => {
    appendMessage(msg.role, msg.content);
  });
}
//Este apartado se encarga de mantener actualizado el historial de conversaciones
async function refreshHistory(autoLoadLatest = false) {
  historyList.innerHTML = "";
  const conversations = await loadConversations(currentUserId);

  conversations.forEach((conversation, index) => {
    const item = document.createElement("li");
    item.className = "cursor-pointer text-blue-600 hover:underline";
    item.innerText = `Conversación ${conversation.id}`;
    //Si uno hace click en una conversacion del historial, se muestra en el chatbox dicho historial de la conversacion seleccionada
    item.addEventListener("click", () => {
      conversationId = conversation.id;
      loadMessages(conversation.id);
    });
    historyList.appendChild(item);

    if (index === 0 && autoLoadLatest) {
      conversationId = conversation.id;
      loadMessages(conversation.id);
    }
  });
}

loginBtn.addEventListener("click", async () => {
  const username = usernameInput.value.trim();
  if (!username) return alert("Debe ingresar un nombre de usuario");

  currentUsername = username.toLowerCase();

  // En este apartado de realiza el login del usuario, por lo que se envia un fetch al endpoint /login de routes.py con el username ingresado en el formulario
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: currentUsername }),
  });

  const data = await res.json();
  //En caso de existir un error en el ingreso o procesamiento de la info, se retorna una alerta al usuario
  if (data.error) return alert(data.error);

  currentUserId = data.user_id;

  loginSection.classList.add("hidden");
  chatSection.classList.remove("hidden");

  await refreshHistory(true);
});


//En este caso se establece la logica para el envio de un mensaje al chatbot (primero pasando por /chat en la API de la app)
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;
  //Al enviar el mensaje, inmediatamente se muestra en el historial siguiendo la logica explicada en appendMessage (en este caso a la derecha y color azul)
  appendMessage("user", message);
  messageInput.value = "";
  //Se envia el mensaje a la API, y se espera a obtener la respuesta del chatbot
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: currentUsername,
      message,
      conversation_id: conversationId,
    }),
  });
  //Nuevamente, si hay error se muestra por alerta
  const data = await res.json();
  if (data.error) return alert(data.error);
  //Una vez recibida la respuesta del chatbot, se muestra por el flujo del chat, siguiendo la logica de appendMessage (gris y a la izquierda)
  conversationId = data.conversation_id;
  appendMessage("assistant", data.response);

  await refreshHistory();
});

newConversationBtn.addEventListener("click", async () => {
  // Nueva conversación solo al enviar primer mensaje (aún no creada aquí)
  conversationId = null;
  clearChat();
});

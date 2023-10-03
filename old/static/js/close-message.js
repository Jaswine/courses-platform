const messages = document.querySelectorAll('.message');
const message_closes = document.querySelectorAll('.message_close');

// Close Message When U Click on Button
for (let i=0; i<messages.length; i++) {
   message_closes[i].onclick = () => {
      messages[i].style.display = 'none';
   }
}

// Close Message When U Click on Escape or Delete
addEventListener('keydown', (e) => {
   for (let i=0; i<messages.length; i++) {
      if (e.key === 'Delete' || e.key === 'Escape') {
         messages[i].style.display = 'none';
      }
   }
})

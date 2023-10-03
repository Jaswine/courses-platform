
const codeRunner = document.querySelector('#runCode');

codeRunner.addEventListener('click', ( ) => {
   let outputDiv = document.querySelector('#output');
   let editor = document.querySelector('#editor').value
   
      let result = eval(editor)

   try {
      outputDiv.innerHTML = result;
   } catch (e) {
      outputDiv.innerHTML = e.message;
   }
})
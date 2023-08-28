
const codeRunner = document.querySelector('#runCode');

codeRunner.addEventListener('click', ( ) => {
   console.log('Running code...');
   let outputDiv = document.querySelector('#output');
   let editor = document.querySelector('#editor').value
   
      let result = eval(editor)
   console.log(result)

   try {
      outputDiv.innerHTML = result;
   } catch (e) {
      outputDiv.innerHTML = e.message;
   }
})
import {createGlobalMessage} from "./globalMessage.js";

export async function sendData (path, data) {
 await fetch(path, {
        method: 'POST',
        body: data
    })
        .then(response => response.json())
        .then(d => {
            console.log(d)
            createGlobalMessage(d.message)
        })
        .catch(error => {
            console.error('ERROR: \n\n', error)
        })
}
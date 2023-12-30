// online ASCII Calculator

let div = document.querySelector('div');
let pre = document.querySelector('pre');
let form = document.querySelector('form');
let input = document.querySelector('input');
let text = document.querySelector('p');
let output = document.getElementById('output');

input.addEventListener('keypress' , handler);
input.addEventListener('focus' , focusHandler);
form.addEventListener('reset' , resetHandler);

input.focus();

function focusHandler(event){
    event.target.select();
};

let split_text = pre.innerHTML.split(' ');
let color_text = [];
let word_count = 0;

// remove unusable characters from text words
for (let i in split_text) {
	split_text[i] = split_text[i].replace('\n', '');	
	split_text[i] = split_text[i].replace('\t', '');
}

function handler(event){
    if(event.key == ' '){
		console.log(split_text[0]);
		console.log(input.value);
		if ((input.value.replace(' ','')) == split_text[0])
		{
			pre.innerHTML = '';

			color_text.push( split_text.shift() );
			pre.innerHTML += "<span style='color:green;margin-top:100px;'>"; 
			for (let i in color_text) {
				pre.innerHTML += `<span style='color:green;'>${color_text[i]}</span> `;	
			}
			for (let i in split_text) {

				pre.innerHTML += split_text[i] + ' ';
			}
			
			word_count++;
			input.value = '';
		}
		else 
		{
			alert(` wrong word ${input.value} `);
			input.value = '';
		}

    }
}

function resetHandler(event){
    text.textContent = '';
};


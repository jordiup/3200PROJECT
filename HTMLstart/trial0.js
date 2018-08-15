function printer()
{
	var text = document.getElementById('tb').value;
	var old = document.getElementById('printer').innerHTML;
	document.getElementById('printer').innerHTML = old + "<br>" + text;
}

//note: can not use clear() as it is a built-in function
function wipe()
{
	document.getElementById('printer').innerHTML = "";
}

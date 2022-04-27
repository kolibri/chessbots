document.addEventListener("DOMContentLoaded", function() {

    var form = document.getElementById('post-json');
    form.onsubmit = function(event){
        event.preventDefault();
        var xhr = new XMLHttpRequest();
        console.log(form)
        var formData = form.querySelector('textarea[name="data"]').value;

        console.log(formData);


        xhr.open('POST', form.action)
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(formData);

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                form.reset();

                var msgBox = document.createElement('pre');
                msgBox.appendChild(document.createTextNode(xhr.status + ": " + xhr.response))
                form.append(msgBox)
                console.log(xhr.status, xhr.responseText)
            }
        }
        return false;
    }

    var filter_form = document.getElementById('bot-filter');
    filter_form.onsubmit = function(event){
        event.preventDefault();
        var xhr = new XMLHttpRequest();
        var filter = filter_form.querySelector('input[name="filter"]').value;

        console.log(filter);
        xhr.open('GET', filter_form.action + '?' + filter)
        xhr.send();

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                filter_form.reset();

                var msgBox = document.createElement('pre');
                msgBox.appendChild(document.createTextNode(xhr.status + ": " + xhr.response))
                filter_form.append(msgBox)
                console.log(xhr.status, xhr.responseText)
            }
        }
        return false;
    }
});

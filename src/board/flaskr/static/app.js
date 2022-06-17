document.addEventListener("DOMContentLoaded", function() {
    function register(data) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action)
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(data);

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                form.reset();

                var msgBox = document.createElement('pre');
                msgBox.appendChild(document.createTextNode(xhr.status + ": " + xhr.response))
                form.append(msgBox)
                console.log(xhr.status, xhr.responseText)
            }
        }
    }

    var form = document.getElementById('post-json');
    var filter_form = document.getElementById('bot-filter');
    var response_box = document.createElement('div');

    form.onsubmit = function(event){
        event.preventDefault();
        var formData = form.querySelector('textarea[name="data"]').value;
        register(formData)
        return false;
    }

    function send_bot_action(method, action, filter) {
        var xhr = new XMLHttpRequest();

        xhr.open(method, action + '?' + filter)
        xhr.send();

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                filter_form.reset();
                filter_form.querySelector('input[name="filter"]').value = filter;

                var msgBox = document.createElement('pre');
                msgBox.appendChild(document.createTextNode(xhr.status + ": " + xhr.response))

                data = JSON.parse(xhr.response);
                new_response = debug_bots_list(data)
                response_box.innerHTML = ''
                response_box.appendChild(new_response)

//                filter_form.replaceChild(new_response, response_box)
                //console.log(xhr.status, xhr.responseText)
            }
        }
        return false;
    }

    filter_form.append(response_box);
    filter_form.onsubmit = function(event) {
        event.preventDefault();
        var action = event.submitter.dataset.action
        var method = event.submitter.dataset.method
        var filter = filter_form.querySelector('input[name="filter"]').value;
        console.log(action, method, filter)
        send_bot_action(method, action, filter)
    }

    send_bot_action('get', '/bots', '')

    var filter_presets = document.getElementById('bot-filter-presets')
    selector = "#bot-filter-presets span"
    elementList = document.querySelectorAll(selector)
    elementList.forEach(function(node, idx) {
//        console.log(node, idx)

        node.addEventListener('click', function(event){
            event.preventDefault()
            send_bot_action('get', '/bots', event.srcElement.dataset.filter)
        })
    });

    function debug_bots_list(bots) {
        var container = document.createElement('div')
        container.classList.add('debug-bots-list');

        for (bot of bots) {
            container.append(transform_bot_to_debug_view(bot))
        }

        return container
    }

    function transform_bot_to_debug_view(bot) {

        var container = document.createElement('div')
        var title = document.createElement('h3')
        title.appendChild(document.createTextNode(bot.name ? bot.name : bot.id))

        var data = document.createElement('dl')
        for (key in bot) {
            var label = document.createElement('dt')
            label.appendChild(document.createTextNode(key))
            label.dataset.state = 0
            label.addEventListener('click', function(event){
                event.preventDefault()
                name = event.target.textContent
                state = event.target.dataset.state
                event.target.dataset.state = 0 == state ? 1 : 0
                selector = "dd[data-key='" + name + "']"
                elementList = document.querySelectorAll(selector)
                elementList.forEach(function(node, idx) {
                    old_class = (0 != state ? 'show' : 'hide');
                    new_class = (0 == state ? 'show' : 'hide');
                    node.classList.add(new_class)
                    node.classList.remove(old_class)
                });
            });

            var value = document.createElement('dd')

            if(key.endsWith('_image')) {
                var link = document.createElement('a')
                link.setAttribute('href', bot[key])
                link.setAttribute('target', '_blank')
                link.appendChild(document.createTextNode(JSON.stringify(bot[key])))

                var img = document.createElement('img')
                img.src = bot[key]
                link.appendChild(img)

                value.appendChild(link)

            } else if ('url' == key || key.endsWith('_url')) {
                var link = document.createElement('a')
                link.setAttribute('href', bot[key])
                link.setAttribute('target', '_blank')
                link.appendChild(document.createTextNode(JSON.stringify(bot[key])))
                value.appendChild(link)
            } else if ('state' == key) {
                if(bot[key] == "offline") {
                    value.classList.add('state-offline')
                }
                value.appendChild(document.createTextNode(JSON.stringify(bot[key])))
            } else {
                value.appendChild(document.createTextNode(JSON.stringify(bot[key])))
            }

            value.dataset.key = key

            data.appendChild(label);
            data.appendChild(value);
        }

        var actions = document.createElement('div')
        actions.classList.add('actions')
        var re_register = document.createElement('a')
        re_register.appendChild(document.createTextNode('re-register'))
        re_register.addEventListener('click', function(event){
            event.preventDefault()
            register('["' + bot.url + '"]')
        });

        actions.appendChild(re_register)
        container.appendChild(title);
        container.appendChild(data);
        container.appendChild(actions);

        return container;
    }
});

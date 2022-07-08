document.addEventListener("DOMContentLoaded", function () {
    function createElement(type, options) {
        var element = document.createElement(type)
        if (options) {
            if (options['attributes'] !== undefined) {
                for (name in options.attributes) {
                    element.setAttribute(name, options.attributes[name])
                }
            }
            if (options['classes'] !== undefined) {
                for (c of options.classes) {
                    element.classList.add(c);
                }
            }
            if (options['id'] !== undefined) {
                element.id = options.id
            }
            if (options['txt'] !== undefined) {
                element.appendChild(document.createTextNode(options.txt))
            }
            if (options['src'] !== undefined) {
                element.src = options.src
            }
            if (options['dataset'] !== undefined) {
                for (d in options.dataset) {
                    element.dataset[d] = options.dataset[d]
                }
            }
            if (options['click'] !== undefined) {
                element.addEventListener('click', options.click)
            }
            if (options['children'] !== undefined) {
                for (child of options.children) {
                    element.appendChild(child)
                }
            }
        }

        return element
    }

    function make_request(method, path, data, handler) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, path)
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(data);

        var output = document.getElementById('xhr_result')
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                console.log(method, path, data, xhr.status, xhr.responseText)
                var row_txt = method + ' ' + path + ' - ' + xhr.status + ": " + xhr.response
                output.append(createElement('pre', {txt: row_txt}))
                handler(xhr)
            }
        }
    }

    function post_register(data) {
        var form = document.getElementById('register_form');
        make_request('POST', form.action, data)
    }

    function send_bot_action(method, action, filter) {
        var filter_form = document.getElementById('bot-filter');
        make_request(method, action + '?' + filter, null, function (xhr) {
            var response_box = filter_form.querySelector('#bots')
            response_box.innerHTML = ''
            response_box.appendChild(create_bots_list(JSON.parse(xhr.response)))
        })
    }

    function create_bots_list(bots) {
        var container = createElement('div', {classes: ['debug-bots-list']})
        for (bot of bots) {
            container.append(transform_bot_to_debug_view(bot))
        }
        return container
    }

    function transform_bot_to_debug_view(bot) {
        function createListItem(key, value) {
            var label = createElement('dt', {
                txt: key,
                dataset: {show: 0},
                click: function (event) {
                    event.preventDefault()
                    var state = event.target.dataset.show
                    event.target.dataset.show = 0 == state ? 1 : 0
                }
            })

            var data = {dataset: {key: key}}
            if ('id' == key) {
                data.txt = JSON.stringify(value)
                data.click = function (event) {
                    send_bot_action('get', '/bots', 'id=' + value)
                }

            } else if (key.endsWith('_image')) {
                data.children = [
                    createElement('a', {
                        attributes: {'href': value, 'target': '_blank'},
                        txt: JSON.stringify(value),
                        children: [createElement('img', {src: value})]
                    })]
            } else if ('url' == key || key.endsWith('_url')) {
                data.children = [createElement('a', {
                    attributes: {'href': value, 'target': '_blank'},
                    txt: JSON.stringify(value)
                })]
            } else if ('motors' == key) {
                data.txt = JSON.stringify(value)
            } else {
                data.txt = value
            }
            return [label, createElement('dd', data)]
        }

        var id = bot.name ? bot.name : bot.id
        var list_items = []
        for (key in bot) {
            list_items.push(...createListItem(key, bot[key]))
        }

        var container = createElement('div', {
            dataset: {botid: id, big: 0},
            children: [
                createElement('h3', {txt: id}),
                createElement('dl', {children: list_items}),
                createElement('div', {
                    classes: ['actions'],
                    children: [createElement('button', {
                        txt: 're-register',
                        click: function (event) {
                            event.preventDefault()
                            post_register('["' + bot.url + '"]')
                        }
                    })]
                })
            ]
        })
        return container;
    }

    function attach_register_handler() {
        var form = document.getElementById('register_form');
        form.onsubmit = function (event) {
            event.preventDefault();
            var formData = form.querySelector('textarea[name="data"]').value;
            post_register(formData)
            return false;
        }
    }

    function attach_filter_handler() {
        var filter_form = document.getElementById('bot-filter');
        filter_form.appendChild(createElement('div', {id: 'bots'}))
        filter_form.onsubmit = function (event) {
            event.preventDefault();
            var action = event.submitter.dataset.action
            var method = event.submitter.dataset.method
            var filter = filter_form.querySelector('input[name="filter"]').value;
            send_bot_action(method, action, filter)
        }

        var elementList = document.querySelectorAll("#bot-filter-presets span")
        elementList.forEach(function (node, idx) {
            node.addEventListener('click', function (event) {
                event.preventDefault()
                send_bot_action('get', '/bots', event.srcElement.dataset.filter)
            })
        });

        send_bot_action('get', '/bots', '')
    }

    function attach_xhr() {
        container = document.getElementById('dashboard')
        container.appendChild(createElement('div', {id: 'xhr_result'}))
    }

    function attach_dashboard_tabs() {
        var nav_links = document.querySelectorAll('#dashboard > nav a');
        nav_links.forEach(function (link, idx) {
            link.addEventListener('click', function (event) {
                var sections = document.querySelectorAll('#dashboard > section[data-show]');
                sections.forEach(function (section, idx) {
                    section.dataset.show = '0'
                });

                document.querySelector('#dashboard > section' + link.attributes.href.value).dataset.show = '1';
            })
        });
    }

    attach_xhr()
    attach_dashboard_tabs()
    attach_register_handler()
    attach_filter_handler()
});

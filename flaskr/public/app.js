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

            if (options['style'] !== undefined) {
                element.style.cssText = options.style
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
                // console.log(method, path, data, xhr.status, xhr.responseText)
                var row_txt = method + ' ' + path + ' - ' + xhr.status + ": " + xhr.response
                output.append(createElement('pre', {txt: row_txt}))
                if (handler) {
                    handler(xhr)
                }
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

            } else if (key.startsWith('image_')) {
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

    function attach_botrc_handler() {
        var rc_form = document.getElementById('botrc');
        rc_form.onsubmit = function (event) {
            event.preventDefault();
            var action = rc_form.querySelector('input[name="bot_address"]').value;
            var method = 'post'
            var data = rc_form.querySelector('textarea[name="sequence"]').value;
            make_request(method, action, data)
        }
    }

    function create_board_pieces_list_item(piece_data) {
        // console.log('cb', piece_data)
        var classList =  piece_data.found ? ['piece-item', 'found', piece_data.piece] : ['piece-item', piece_data.piece]

        info = piece_data.found ? piece_data.bot.captcha_data.pos: 'Not found'

        return createElement(
            'div',
            {
                classes: classList,
                children: [
                    createElement('span', {classes: ['title'], txt: piece_data.piece}),
                    createElement('span', {classes: ['field'], txt: piece_data.field})
                ]
            }
        )
    }

    function add_board_bot(bot, found) {
        console.log('add_board_bot', bot,  bot['name'])
        var classes = ['bot']

        if (found) {
            classes.push('found')
        }
        if (bot['http_data']['piece']) {
            classes.push(bot['http_data']['piece'])
        }

        var bot_el = createElement('span', {txt: bot.http_data.name, classes: classes})
        if (0 < Object.keys(bot['captcha_data']).length) {
            var pos = bot.captcha_data.pos
            var mult = 5
            var subt = 10

            var pos_bott = (pos[1]*mult)-subt
            var pos_left = (pos[0]*mult)-subt
            var rot = bot.captcha_data.rotation
            var css_test = 'bottom: ' + pos_bott + 'px; left: ' + pos_left + 'px; transform: rotate(' + rot + 'deg);'
            bot_el.style.cssText = css_test
        }
        return bot_el
    }

    function build_board_data(data) {
        function find_piece_for_field(field, pieces) {
            for (var p of pieces) {
                if (field[0] == p.field[0] && field[1] == p.field[1]) {
                    return p
                }
            }
            return false
        }
        var board_div = document.getElementById('board')
        var files = ['z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']
        var ranks = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].reverse()
        var board_view = createElement('div', {classes: ['board-view']})
        for (var r of ranks) {
            var board_file = createElement('div', {classes: ['column']})
            for (var f of files) {
                var classes = ['field', f + 'x' + r]

                if (piece = find_piece_for_field([f, r], data.board.pieces)) {
                    classes.push('piece')
                    classes.push(piece.piece)
                    if (piece.found) {
                        classes.push('found')
                    }
                }

                var board_field = createElement('div', {classes: classes})

                board_file.appendChild(board_field)
            }
            board_view.appendChild(board_file)
        }

        var board_bots = createElement('div', {classes: ['board-bots']})
        for (var bot of data.board.rest_bots) {
            board_bots.appendChild(add_board_bot(bot, false))
        }
        var pieces_list = createElement('div', {classes: ['pieces']})
        for (var piece of data.board.pieces) {
            pieces_list.appendChild(create_board_pieces_list_item(piece))
            if (piece.found) {
                board_bots.appendChild(add_board_bot(piece.bot, true))
            }
        }

        var status_classes = ['status']
        var status_text = 'Error. Not playable'
        if (true == data.playable) {
            status_classes.push('playable')
            status_text = 'Playable :)'
        }
        var playable_status = createElement('div', {txt: status_text, classes: status_classes})

        board_div.appendChild(playable_status)
        board_div.appendChild(pieces_list)
        board_div.appendChild(board_view)
        board_div.appendChild(board_bots)
    }

    function update_board() {
        var board_data = document.querySelectorAll('#board > :not(nav)');
        board_data.forEach(function (data_element, idx) {
            data_element.remove()
        })

        make_request('GET', '/bots/board', null, function (xhr) {
            build_board_data(JSON.parse(xhr.response))
        })
    }

    attach_xhr()
    attach_dashboard_tabs()
    attach_filter_handler()
    attach_register_handler()
    attach_botrc_handler()
    update_board()
});

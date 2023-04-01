import React, {useState, useEffect, useRef} from 'react';

function piecename_to_unicode(piecename) {
    const map = {
        'wk': '\u2654',
        'wq': '\u2655',
        'wb': '\u2657',
        'wn': '\u2658',
        'wr': '\u2656',
        'wp': '\u2659',
        'bk': '\u265A',
        'bq': '\u265B',
        'bb': '\u265D',
        'bn': '\u265E',
        'br': '\u265C',
        'bp': '\u265F',
    }
    if (!Object.keys(map).includes(piecename)) {
        return piecename
    }
    return map[piecename]
}



/*
function Mailbox(props) {
  const unreadMessages = props.unreadMessages;
  return (
    <div>
      <h1>Hello!</h1>
      {unreadMessages.length > 0 &&
        <h2>
          You have {unreadMessages.length} unread messages.
        </h2>
      }
    </div>
  );
}
*/

async function get_board() {
    try {
        const response = await fetch('http://127.0.0.1:8031/board/'); // @todo: hardcoded url, only path should be needed
        return await response.json();
    } catch (error) {
        return [];
    }
}

async function get_mockbots() {
    try {
        const response = await fetch('http://127.0.0.1:8031/mockbot/'); // @todo: hardcoded url, only path should be needed
        return await response.json();
    } catch (error) {
        return [];
    }
}

async function update_bot(bot) {
    try {
         // @todo: hardcoded url, only path should be needed
        const response = await fetch('http://127.0.0.1:8031/bots/?slug=' + bot.slug, {method: 'PATCH'});
        console.log('update bot', bot.slug, response.json())
        return await response.json();
    } catch (error) {
        return [];
    }
}


async function register_bots(bots) {
    try {
         // @todo: hardcoded url, only path should be needed
        const response = await fetch('http://127.0.0.1:8031/bots/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(bots)
        });
        return await response.json();
    } catch (error) {
        return [];
    }
}

async function create_mockbot(data) {
    try {

         // @todo: hardcoded url, only path should be needed
        console.log('request done', data)
        const response = await fetch('http://127.0.0.1:8031/mockbot/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        return [];
    }

}

const Piece = (data, index, display_bot) => {
    let botName = ''
    if (data.found) {
        botName = <span className='bot-name' onClick={(e) => display_bot(data.bot)}>{data.bot.http_data.name}</span>
    }
    return (
        <span key={index} className='piece' data-found={data.found}>
            <span className='title'>{piecename_to_unicode(data.piece)}</span>
            <span className='field'>{data.field}</span>
            {botName}
          </span>
    )
}

const RestBot = (data, index, display_bot) => {
    return (
        <span key={index} className='rest-bot'>
            <span className='title' onClick={(e) => display_bot(data)}>{data.url}</span>
        </span>
    )
}

const BotDisplay = (bot, update_bot) => {
    return (
        <div className='bot-display' key='bot-display'>
            <a className='link' key='link' href={bot.url}>{bot.url}</a>
            <span className='piece' key='piece'>{bot.http_data ? piecename_to_unicode(bot.http_data.piece) : ''}</span>
            <span className='position'
                  key='position'>{bot.captcha_data && bot.captcha_data.pos ? bot.captcha_data.pos[0] + 'x' + bot.captcha_data.pos[1] : ''}</span>
            <span className='rotation' key='rotation'>{bot.captcha_data ? bot.captcha_data.rotation : ''}</span>
            <img className='pos_pic_cache_url' key='pos_pic_cache_url'
                 src={bot.http_data ? bot.http_data.pos_pic_cache_url : ''}/>
            <button onClick={(e) => update_bot(bot)} >update</button>
        </div>
    )
}

const BotPosition = (bot, display_bot) => {
    const piece_symbol = bot.http_data && bot.http_data.piece ? piecename_to_unicode(bot.http_data.piece) : '?'

    let styles = {'display': 'none'}
    if (bot.captcha_data && bot.captcha_data.pos) {
        const mult = 0.5
        const sub = 2.5


        const pos_bott = (bot.captcha_data.pos[1] * mult) - sub
        const pos_left = (bot.captcha_data.pos[0] * mult) - sub

        const rot = bot.captcha_data.rotation
        styles = {'bottom': pos_bott + 'vh', 'left': pos_left + 'vh', 'transform': 'rotate(' + rot + 'deg)'}
    }

    return (
        <span className='bot-position' key={bot.slug} style={styles} onClick={(e) => display_bot(bot)}>
            {piece_symbol}
        </span>
    )
}

const MockBot = (bot, load_mockbot, register_bot) => {
    return (
        <span className='mockbot' key={bot.name}>
            <button className='btn-load' key='load' onClick={(e) => load_mockbot(bot)}>load</button>
            <button className='btn-register' key='register' onClick={(e) => register_bot(bot)}>register</button>
            <span className='piece' key='piece'>{piecename_to_unicode(bot.piece)}</span>
            <span className='pos' key='pos'>{bot.pos[0]}x{bot.pos[1]}</span>
            <span className='angle' key='angle'>{bot.angle}</span>
            <span className='name' key='name'>{bot.name}</span>
        </span>
    )
}

function App() {
    const [http_data, setHttpData] = useState({})
    const [mockbots_data, setMockBotsData] = useState({})
    const [selected_bot, setSelectedBot] = useState({})
    const registerBotsRef = useRef()
    const [mockbot_name, setMockbotName ] = useState('')
    const [mockbot_piece, setMockbotPiece ] = useState('')
    const [mockbot_posx, setMockbotPosx ] = useState('')
    const [mockbot_posy, setMockbotPosy ] = useState('')
    const [mockbot_angle, setMockbotAngle ] = useState('')

    const displayBot = (bot) => {
        setSelectedBot(bot)
    }

    const loadMockBot = (bot) => {
        setMockbotName(bot['name'])
        setMockbotPiece(bot['piece'])
        setMockbotPosx(bot['pos'][0])
        setMockbotPosy(bot['pos'][1])
        setMockbotAngle(bot['angle'])
    }

    const updateBot = (bot) => {
        update_bot(bot).then(() => {
            updateBoard()
        })
    }

    const updateBoard = () => {
        get_board().then(board => {
            setHttpData(board)
        })
    }

    const registerBot = () => {
        const area_content = registerBotsRef.current.value.split('\n')
        register_bots(area_content).then(() => {
            updateBoard()
        })
    }

    const registerMockBot = (bot) => {
        const area_content = registerBotsRef.current.value.split('\n')
        register_bots([bot.url]).then(() => {
            updateBoard()
        })
    }

    const handleMockBotName = (event) => { setMockbotName(event.target.value); };
    const handleMockBotPiece = (event) => { setMockbotPiece(event.target.value); };
    const handleMockBotPosx = (event) => { setMockbotPosx(event.target.value); };
    const handleMockBotPosy = (event) => { setMockbotPosy(event.target.value); };
    const handleMockBotAngle = (event) => { setMockbotAngle(event.target.value); };

    const createMockBot = () => {
        if ('' === mockbot_name ||
            '' === mockbot_piece ||
            '' === mockbot_posx ||
            '' === mockbot_posy ||
            '' === mockbot_angle
        ) {
            console.log('invalid form data')
            return
        }

        const data = {
            name: mockbot_name,
            piece: mockbot_piece,
            pos: [parseInt(mockbot_posx), parseInt(mockbot_posy)],
            angle: parseInt(mockbot_angle)
        }

            console.log('create bot', data)
        create_mockbot(data).then((bot_data) => {
            register_bots([bot_data['url']]).then(() => {
                updateBoard()
                getMockBots()
            })
        })
    }

    const getMockBots = () => {
        get_mockbots().then((data) => {
            setMockBotsData(data)
        })
    }

    useEffect(() => {
        get_board().then(board => {
            setHttpData(board)
        })
        get_mockbots().then((data) => {
            setMockBotsData(data)
        })

    }, [])

    let fields = []
    let files = ['z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']
    let ranks = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for (const r of ranks) {
        for (const f of files) {
            fields.push([f, r])
        }
    }

    let pieces = <li>Empty list</li>
    let restBots = ''
    let bot_display = ''
    let position_bots = ''
    let mockbot_items = <li>Empty list</li>
    if (http_data && http_data.board) {
        pieces = http_data.board.pieces.map((piece, index) => Piece(piece, index, displayBot))
        restBots = http_data.board.rest_bots.map((bot, index) => RestBot(bot, index, displayBot))
        position_bots = http_data.bots.map((bot, index) => BotPosition(bot, displayBot))
    }

    if (selected_bot) {
        bot_display = BotDisplay(selected_bot, updateBot)
    }

    // if () {
    //
    // }
    if (0 < mockbots_data.length) {
        mockbot_items = mockbots_data.map((bot, index) => MockBot(bot, loadMockBot, registerMockBot))
    }

    return (
        <div>
            <div className='pieces-overview' key='pieces-overview'>
                <div className='pieces' key='pieces'>
                    {pieces}
                </div>
                <div className='rest-bots' key='rest-bots'>
                    {restBots}
                </div>
                {bot_display}
            </div>
            <div className='board' key='board'>
                {fields.map((field) =>
                    <span key={field[0] + field[1]} data-rank={field[0]} data-file={field[1]} className='field'>
                        {field[0] + field[1]}
                    </span>
                )}
            </div>
            <div className='bot-positions' key='bot-positions'>
                {position_bots}
            </div>

            <div className='register-bot' key='register-bot'>
                <textarea name='register-bot-input' ref={registerBotsRef}></textarea>
                <button onClick={(e) => registerBot()}>register</button>
            </div>
            <div className='create-mockbot' key='create-mockbot'>
                <form key='mockbot-form'>
                    <input placeholder='name' className='create-mockbot-name' key='create-mockbot-name' value={mockbot_name} onChange={handleMockBotName} />
                    <input placeholder='piece' className='create-mockbot-piece' key='create-mockbot-piece' value={mockbot_piece} onChange={handleMockBotPiece} />
                    <input placeholder='posx' className='create-mockbot-posx' key='create-mockbot-posx' value={mockbot_posx} onChange={handleMockBotPosx} />
                    <input placeholder='posy' className='create-mockbot-posy' key='create-mockbot-posy' value={mockbot_posy} onChange={handleMockBotPosy} />
                    <input placeholder='angle' className='create-mockbot-angle' key='create-mockbot-angle' value={mockbot_angle} onChange={handleMockBotAngle} />
                    <button onClick={(e) => createMockBot()}>create mockbot</button>
                </form>
                <div className='mockbot-list' key='mockbot-list'>
                    {mockbot_items}
                </div>
            </div>
        </div>
    )
}

export default App;



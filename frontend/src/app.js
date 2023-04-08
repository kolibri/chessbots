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
    let botName = <span className='bot-name'>test_wb</span>
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
            <span className='title' onClick={(e) => display_bot(data)}>{data.http_data ? data.http_data.name : data.url}</span>
        </span>
    )
}

const ImgLink = (data) => {
    // console.log(data)
    if (data.src) {
        return (
            <a href={data.src} className='img' target='_blank'>
                <img className='pos_pic' src={data.src} alt={data.alt} />
            </a>
        )
    }
    return (<span className='img_placrholder'></span>)
}
const BotDisplay = (bot, update_bot) => {
    return (
        <div className='bot-display' key='bot-display'>
            <button onClick={(e) => update_bot(bot)} >update</button>
            <a className='link' key='link' href={bot.url}>{bot.http_data ? bot.http_data.name : bot.url}</a>
            <span className='piece' key='piece'>{bot.http_data ? piecename_to_unicode(bot.http_data.piece) : ''}</span>
            <span className='position'
                  key='position'>{bot.captcha_data && bot.captcha_data.pos ? bot.captcha_data.pos[0] + 'x' + bot.captcha_data.pos[1] : ''}</span>
            <span className='rotation' key='rotation'>{bot.captcha_data ? bot.captcha_data.rotation : ''}</span>
            {ImgList(bot)}
        </div>
    )
}

const ImgList = (bot) => {
    return (
        <div className='img-list' key='img-list'>
            <ImgLink src={bot.http_data ? bot.http_data.pos_pic_cache_url : false} alt='raw' key='pos_pic_cache_url' />
            {bot.debug && bot.debug.imgs && bot.debug.imgs.map((f, i) =>
                <ImgLink src={f[1]} alt={f[0]} key={f[0]} />
            )}
        </div>
    )
}

const BotPosition = (bot, display_bot) => {
    const piece_symbol = bot.http_data && bot.http_data.piece ? piecename_to_unicode(bot.http_data.piece) : '?'

    let styles = {'display': 'none'}
    if (bot.captcha_data && bot.captcha_data.pos) {
        const mult = 0.5
        // const sub = 2.5


        const pos_bott = (bot.captcha_data.pos[1] * mult) //- sub
        const pos_left = (bot.captcha_data.pos[0] * mult) //- sub

        const rot = bot.captcha_data.rotation
        styles = {'bottom': pos_bott + '%', 'left': pos_left + '%', 'transform': 'rotate(' + rot + 'deg)'}
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

const RegisterDashboard = (bots_data, register_bots, registerBotsRef, handle_mockbot_data_change, create_mockbot, load_mockbot, register_mockbot, form_data) => {
    // console.log('mockbot_data', mockbot_data)
    return (
        <div className='register-dashboard' key='register-dashboard'>
            <form className='register' key='register'>
                <textarea name='bots' ref={registerBotsRef}></textarea>
                <button onClick={(e) => register_bots(e)} type='none'>GO</button>
            </form>
            <form className='mockbot' key='mockbot-form'>
                <input placeholder='name' name='name' key='name' type='text' value={form_data.name} onChange={handle_mockbot_data_change} />
                <input placeholder='piece' name='piece' key='piece' type='text' value={form_data.piece} onChange={handle_mockbot_data_change} />
                <input placeholder='posx' name='posx' key='posx' type='number' value={form_data.posx} onChange={handle_mockbot_data_change} />
                <input placeholder='posy' name='posy' key='posy' type='number' value={form_data.posy} onChange={handle_mockbot_data_change} />
                <input placeholder='angle' name='angle' key='angle' type='number' value={form_data.angle} onChange={handle_mockbot_data_change} />
                <button onClick={(e) => create_mockbot(e)}>ok</button>
            </form>
            <div className='mockbot-list' key='mockbot-list'>
                {0 < bots_data.length && bots_data.map((bot, index) => MockBot(bot, load_mockbot, register_mockbot))}
            </div>
       </div>
    )
}

function App() {
    const [http_data, setHttpData] = useState({})
    const [mockbots_data, setMockBotsData] = useState({})
    const [selected_bot, setSelectedBot] = useState({})
    const registerBotsRef = useRef()
    const [mockbot_data, setMockbotData ] = useState({
        name: null,
        piece: null,
        posx: null,
        posy: null,
        angle: null,
    })

    const displayBot = (bot) => {
        setSelectedBot(bot)
    }

    const loadMockBot = (bot) => {
        console.log('set bot', bot)
        setMockbotData({
            name: bot.name,
            piece: bot.piece,
            posx: bot.pos[0],
            posy: bot.pos[1],
            angle: bot.angle,
        })
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

    const registerBot = (e) => {
        e.preventDefault()
        const area_content = registerBotsRef.current.value.split('\n')
        // console.log(area_content)
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

    const handleMockBotChange = (event) => {
        console.log(event.target)
        setMockbotData({
            ...mockbot_data,
            [event.target.name]: event.target.value,
        })
    };

    const createMockBot = (e) => {
        e.preventDefault()
        if ('' === mockbot_data.name ||
            '' === mockbot_data.piece ||
            '' === mockbot_data.posx ||
            '' === mockbot_data.posy ||
            '' === mockbot_data.angle
        ) {
            console.log('invalid form data')
            return
        }

            console.log('create bot', {
                name: mockbot_data.name,
                piece: mockbot_data.piece,
                pos: [mockbot_data.posx, mockbot_data.posy],
                angle: mockbot_data.angle,
            })
        create_mockbot({
                name: mockbot_data.name,
                piece: mockbot_data.piece,
                pos: [parseInt(mockbot_data.posx), parseInt(mockbot_data.posy)],
                angle: parseInt(mockbot_data.angle),
            }).then((bot_data) => {
            // register_bots([bot_data['url']]).then(() => {
            //     updateBoard()
            //     getMockBots()
            // })
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
    for (const f of files) {
        for (const r of ranks) {
            fields.push([r, f])
        }
    }

    return (
        <div className='dashboard'>
            <div className='pieces-overview' key='pieces-overview'>
                <div className='pieces' key='pieces'>
                    {http_data && http_data.board && http_data.board.pieces.map((piece, index) => Piece(piece, index, displayBot))}
                </div>
                <div className='rest-bots' key='rest-bots'>
                    {http_data && http_data.board && http_data.board.rest_bots.map((bot, index) => RestBot(bot, index, displayBot))}
                </div>
            </div>
            <div className='board' key='board'>
                <div className='board-fields'>
                    {fields.map((field) =>
                        <span key={field[0] + field[1]} data-rank={field[0]} data-file={field[1]} data-name={field[1] + '' + field[0]} className='field'>
                            {field[1] + field[0]}
                        </span>
                    )}
                </div>
                <div className='bot-positions' key='bot-positions'>
                    {http_data && http_data.board && http_data.bots.map((bot, index) => BotPosition(bot, displayBot))}
                </div>
            </div>
            {selected_bot && BotDisplay(selected_bot, updateBot)}
            {RegisterDashboard(mockbots_data, registerBot, registerBotsRef, handleMockBotChange, createMockBot, loadMockBot, registerMockBot, mockbot_data)}

        </div>
    )
}

export default App;



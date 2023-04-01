import React, {useState, useEffect} from 'react';

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
    return map[piecename]
}

async function get_board() {
    try {
        const response = await fetch('http://127.0.0.1:8031/board/');
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

const BotDisplay = (bot) => {
    return (
        <div className='bot-display' key='bot-display'>
            <a className='link' key='link' href={bot.url}>{bot.url}</a>
            <span className='piece' key='piece'>{bot.http_data ? piecename_to_unicode(bot.http_data.piece) : ''}</span>
            <span className='position' key='position'>{bot.captcha_data && bot.captcha_data.pos ? bot.captcha_data.pos[0] + 'x' + bot.captcha_data.pos[1] : ''}</span>
            <span className='rotation' key='rotation'>{bot.captcha_data ? bot.captcha_data.rotation : ''}</span>
            <img className='pos_pic_cache_url' key='pos_pic_cache_url' src={bot.http_data ? bot.http_data.pos_pic_cache_url : ''} />
        </div>
    )
}

const BotPosition = (bot, display_bot) => {
    const piece_symbol = bot.http_data && bot.http_data.piece ? piecename_to_unicode(bot.http_data.piece) : '?'

    let styles = {'display': 'none'}
    if (bot.captcha_data && bot.captcha_data.pos) {
        const mult = 0.5
        const sub = 2.5


        const pos_bott = (bot.captcha_data.pos[1]*mult)-sub
        const pos_left = (bot.captcha_data.pos[0]*mult)-sub

        const rot = bot.captcha_data.rotation
        styles = {'bottom': pos_bott + 'vh', 'left': pos_left + 'vh','transform': 'rotate(' + rot + 'deg)'}
    }

    return (
        <span className='bot-position' key={bot.slug} style={styles} onClick={(e) => display_bot(bot)}>
            {piece_symbol}
        </span>
    )
}

function App() {
    const [http_data, setHttpData] = useState({})
    const [selected_bot, setSelectedBot] = useState({})

    const displayBot = (bot) => {
        console.log('bot change', bot)
        setSelectedBot(bot)
    }

    const updateBoard = () => {
        get_board().then(board => {
            setHttpData(board)
        })
    }

    useEffect(() => {
        get_board().then(board => {
            setHttpData(board)
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
    if (http_data && http_data.board) {
        pieces = http_data.board.pieces.map((piece, index) => Piece(piece, index, displayBot))
        restBots = http_data.board.rest_bots.map((bot, index) => RestBot(bot, index, displayBot))
        position_bots = http_data.bots.map((bot, index) => BotPosition(bot, displayBot))
    }

    if (selected_bot) {
        bot_display = BotDisplay(selected_bot)
    }



    return (
        <div>

            <div className='controls' key='controls'>
                <button key='update' onClick={(e) => updateBoard()}>update</button>
            </div>
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
        </div>
    )
}

export default App;



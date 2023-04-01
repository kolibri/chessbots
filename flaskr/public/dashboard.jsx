document.addEventListener('DOMContentLoaded', function ()
{
    console.log('BOARD HELLO')
    class Board extends React.Component {
    constructor(props) {
        super(props)
        // let moves = this.adapter.moves;

        this.state = {
            loaded: false,
        }

        // this.gotoMove = this.gotoMove.bind(this);
    }


    // gotoMove(moveIndex) {
    //     this.setState({ply: moveIndex});
    // }

    render() {
        let fields = []
        let files = ['z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']
        let ranks = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].reverse()
        for (const r of ranks) {
            for (const f of files) {
                fields.push([r, f])
            }
        }

        console.log('FIELDS:', fields)
        return (
            <div className='board'>
                {fields.map((field) =>
                    <span data-rank={field[0]} data-file={field[1]} />
                )}
            </div>
            )
    }
}


    const domContainer = document.querySelector('#board');
    const root = ReactDOM.createRoot(domContainer);
    root.render(<Board />);

})
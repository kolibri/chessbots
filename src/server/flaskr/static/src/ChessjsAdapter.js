import Chess from 'chess.js';

export default class ChessjsAdapter {
    constructor(pgn) {
        this.chess = new Chess();
        console.log(pgn)
        this.chess.reset();
        if (typeof pgn !== 'undefined') {
            console.log(this.chess.load_pgn(pgn.trim().replace(/^\s+/gm, '')))
            if (!this.chess.load_pgn(pgn.trim().replace(/^\s+/gm, ''))) {
                console.log('Error loading pgn', pgn);
            }
        }

        this.moves = this.chess.history({ verbose: true });
    }

    info() {
        return this.chess.header();
    }

    // ply = -1 will return start position
    fields(ply) {
        if (ply > this.moves.length) {
            console.log('ply to high', ply, this.moves.length);
            return;
        }        

        this.chess.reset();
        if (!(ply < 0)) {
            for (let n = 0; n < ply+1; n++) {
                this.chess.move(this.moves[n]);
            }
        }

        let i = 0;
        let fieldNames = [];
        for (let r of ['8', '7', '6', '5', '4', '3', '2', '1']) {
            for (let c of ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) {
                fieldNames[i] = c+r;
                i++;
            }
        }

        return fieldNames.map((fieldName) => ({ 
            key: fieldName,
            piece: this.chess.get(fieldName) 
        }))        
    }

    field(ply, fieldName) {
        let fields = this.fields(ply);
        for (let field of fields) {
            if (field.key === fieldName) {
                return field;
            }
        }

        return null;
    }

    getMove(ply){
        return this.moves[ply] ? this.moves[ply] : null;
    }

    makeMove(ply, move) {
        this.chess.reset();

        for (let n = 0; n < ply+1; n++) {
            this.chess.move(this.moves[n]);
        }

        if (null == this.chess.move(move)) {
            return null;
        }

        this.moves = this.chess.history({verbose: true});

        return this.moves;
    }

    translateMoves(pieceNames, moves) {
        function formatMove(move) {            
            if (!move) {
                return;
            }

            var moveString = ''

            if (0 <= move.flags.indexOf('k')) { 
                moveString = 'O-O'
            } else if (0 <= move.flags.indexOf('q')) {
                moveString = 'O-O-O'
            } else {
            moveString = pieceNames[move.piece] +                                              // piece name
                move.from  +                                                                   // from field
                ((0 <= move.flags.indexOf('c') || 0 <= move.flags.indexOf('e')) ? 'x' : '-') + // capture sign
                move.to +                                                                      // target field
                ((0 <= move.flags.indexOf('e')) ? 'ep': '') +                                  // en passant
                ((0 <= move.flags.indexOf('p')) ? move.promotion : '' )                        // promotion
            }

            // add check and checkmate flags
            if (0 <= move.san.indexOf('+')) {
                moveString = moveString + '+'
            }
            if (0 <= move.san.indexOf('#')) {
                moveString = moveString + '#'
            }

            return moveString
        }
        
        return moves.map(move => formatMove(move));
    }
}

// dd_MultiplySlowest_50.js
// Multiply slowest moving mv's
var LARGEST = 0;
var SOME_PERCENTAGE = 0.5;
var MULTIPLE = 10;

// global variable holding forward motion vectors from previous frames
var prev_fwd_mvs = [ ];

// change this value to use a smaller or greater number of frmes to average
var tail_length = 20;

function glitch_frame(frame)
{
	LARGEST = 0;
    // bail out if we have no motion vectors
    let mvs = frame["mv"];
    if ( !mvs )
        return;
    // bail out if we have no forward motion vectors
    let fwd_mvs = mvs["forward"];
    if ( !fwd_mvs )
        return;

   	// 1st loop - find the fastest mv
   	// this ends-up in LARGEST as the square of the hypotenuse (mv[0]*mv[0]) + (mv[1]*mv[1])
    let W = fwd_mvs.length;
    for ( let i = 0; i < fwd_mvs.length; i++ )
    {
        let row = fwd_mvs[i];
        // rows
        let H = row.length;
        for ( let j = 0; j < row.length; j++ )
        {
            // loop through all macroblocks
            let mv = row[j];

            // THIS IS WHERE THE MEASUREMENT HAPPENS
            var this_mv = (mv[0] * mv[0])+(mv[1] * mv[1]);
            if ( this_mv > LARGEST){
				LARGEST = this_mv;
			}
        }
    }

    // then find those mv's which are bigger than SOME_PERCENTAGE of LARGEST
    // and then replace them with the average mv from the last n frames
    for ( let i = 0; i < fwd_mvs.length; i++ )
	    {
	        let row = fwd_mvs[i];
	        // rows
	        let H = row.length;
	        for ( let j = 0; j < row.length; j++ )
	        {
	            // loop through all macroblocks
	            let mv = row[j];

	            // THIS IS WHERE THE MAGIC HAPPENS
	            var this_mv = (mv[0] * mv[0])+(mv[1] * mv[1]);
	            if (this_mv < (LARGEST * SOME_PERCENTAGE)){

			     	mv[0] = mv[0] * MULTIPLE;
					mv[1] = mv[1] * MULTIPLE;
				}
	        }
    }
}

// dd_zero.js
// only fuck things up if mv > movement_threshold
var movement_threshold = 3;
function glitch_frame(frame)
{
    // bail out if we have no motion vectors
    let mvs = frame["mv"];
    if ( !mvs )
        return;
    // bail out if we have no forward motion vectors
    let fwd_mvs = mvs["forward"];
    if ( !fwd_mvs )
        return;

    // columns
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

            // THIS IS WHERE THE MAGIC HAPPENS
            if ( (mv[0] * mv[0])+(mv[1] * mv[1]) > movement_threshold*movement_threshold){
	    		//mv[0] = Math.sin(i/W*Math.PI*2)*mv[0];
  	    		//mv[1] = Math.cos(j/H*Math.PI*2)*mv[1];
  	    		mv[0] = 0;//mv[0] * 10;
  	    		mv[1] = 0;//mv[1] * 10;
			}
        }
    }
}

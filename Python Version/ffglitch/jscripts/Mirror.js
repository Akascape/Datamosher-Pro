// dd_mirror_X.js

// clean buffer :
var buffer = [ ];

var ZOOM = -20;

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

	// note that we perform a deep copy of the clean motion
    // vector values before modifying them.
    let json_str = JSON.stringify(fwd_mvs);
    let deep_copy = JSON.parse(json_str);
	// stick em in the buffer
    buffer = deep_copy;

	var M_H = fwd_mvs.length/2;
    // VERTICALLY
    for ( let i = 0; i < fwd_mvs.length; i++ )
    {

        // loop through all rows

        let row = fwd_mvs[i];
        var row2 = buffer[i];
        //var row2 = fwd_mvs[(fwd_mvs.length-1)-i];

        var M_W = row.length/2;

		// HORIZONTALLY
        for ( let j = 0; j < row.length; j++ )
        {
            // loop through all macroblocks
            let mv = row[j];
			var mv2 = row2[(row.length - 1) - j];
            // THIS IS WHERE THE MAGIC HAPPENS
            //if(i>M_W){
				mv[0] = 0-mv2[0];
            	mv[1] = mv2[1];
			//}
        }
    }
}

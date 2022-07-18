// dd_ring_buffer.js
// works kinda like an audio delay
// stacks the previous n frames into a buffer

// global variable holding forward motion vectors from previous frames
var prev_fwd_mvs = [ ];

// change these values to use a smaller or greater number of frames to
// perform the average of motion vectors

// try making the delay long enough to overlap an edit in the content ...
var delay = 10;
// divisor controls "feedback" ... or "feedforward" which ever is a better description ...
var feedback = 0.5;			// a number between 0.000001 and .... yeah - controls how much of the buffered mv gets into the next pass

var divisor = 1.0/feedback;

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

    // update variable holding forward motion vectors from previous
    // frames. note that we perform a deep copy of the clean motion
    // vector values before modifying them.
    let json_str = JSON.stringify(fwd_mvs);
    let deep_copy = JSON.parse(json_str);
    // push to the end of array
    prev_fwd_mvs.push(deep_copy);
    // drop values from earliest frames to always keep the same tail
    // length
    if ( prev_fwd_mvs.length > delay )
        prev_fwd_mvs = prev_fwd_mvs.slice(1);

    // bail out if we still don't have enough frames
    if ( prev_fwd_mvs.length != delay )
        return;

    // replace all motion vectors of current frame with an average
    // of the motion vectors from the previous 10 frames
    for ( let i = 0; i < fwd_mvs.length; i++ )
    {
        // loop through all rows
        let row = fwd_mvs[i];
        let delay_row = prev_fwd_mvs[0][i];
        let insert_row = prev_fwd_mvs[delay-1][i];

        for ( let j = 0; j < row.length; j++ )
        {
            // loop through all macroblocks
            let mv = row[j];
			let dmv = delay_row[j];
            let imv = insert_row[j];
            // THIS IS WHERE THE MAGIC HAPPENS

		// temp copy of the incoming vectors
			let x = mv[0];
			let y = mv[1];
		// pull their replacements out of the buffer
            mv[0] = dmv[0];
            mv[1] = dmv[1];
		// feedback the 'old' with the 'new' for next time
            imv[0] = (dmv[0] / divisor) + x;
            imv[1] = (dmv[1] / divisor) + y;
		// rinse and repeat

        }
    }
}

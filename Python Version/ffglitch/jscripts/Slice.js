// dd_RandomDamage(progZoom).js
// progressive Zoom x and y components of mv if threshold met for frame

let threshold = 95;

var ZOOM = 0;
var doZOOM = 0;
var TRIGGERED = 0;
var nFrames = 5;
var frameCount = 0;

function glitch_frame(frame)
{

	var do_or_not = Math.random() * 100;
	if(do_or_not > threshold){
		if(TRIGGERED > 0){

		}else{
			TRIGGERED = 1;
			frameCount = 0;
			ZOOM = 0;
		}
	}
	// only do the glitch if our random number crosses the threshold
	if(TRIGGERED > 0 & frameCount <= nFrames){
		frameCount++;
		ZOOM+= 10

		var do_dir = Math.random() * 100;
		if(do_dir > 50){
			doZOOM = 0 - ZOOM;
		}else{
			doZOOM = ZOOM
		}
		// bail out if we have no motion vectors
		let mvs = frame["mv"];
		if ( !mvs )
			return;
		// bail out if we have no forward motion vectors
		let fwd_mvs = mvs["forward"];
		if ( !fwd_mvs )
			return;

		var M_H = fwd_mvs.length/2;
		// clear horizontal element of all motion vectors
		for ( let i = 0; i < fwd_mvs.length; i++ )
		{
			// loop through all rows
			let row = fwd_mvs[i];
			var M_W = row.length/2;

			for ( let j = 0; j < row.length; j++ )
			{
				// loop through all macroblocks
				let mv = row[j];

				// THIS IS WHERE THE MAGIC HAPPENS
				// ZOOM X & Y VECTORS
				mv[0] = mv[0] + ((M_W - j) / 10)*doZOOM;
            	mv[1] = mv[1] + ((M_H - i) / 10)*doZOOM;

			}
		}
	}else{
		TRIGGERED = 0;
	}
}

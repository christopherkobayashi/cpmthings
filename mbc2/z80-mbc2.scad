// Z80-MBC2 sandwich case
// Original by Chris Smith (zoharel) http://www.thingiverse.com/thing:3299104

$fs = 0.5;
$fa = 0.5;

width = 100;
height = 100;
thickness = 4;
overlay = 5;
depth = 13;

// The proximity of the screws, on center, to the outside of the board.
screw_margin = 4;
screw_diameter = 2.5;
screw_depth = 20;
support_diameter = 8;

bottom = 0;

// Do the bottom ...
if (bottom == 1)
    bottom();
// ... or do the top
else
    rotate([0,180,0])
        top();

module ventpunch(width,height,depth,hmargin,vmargin,zmargin,hcount,vcount,zcount) {
	hsize = (width+2*hmargin)/hcount;
	vsize = (height+2*vmargin)/vcount;
	zsize = (depth+2*zmargin)/zcount;
    
	translate([-hmargin/2,-vmargin/2,-zmargin/2]) {
		for (horiz = [0 : hcount-1], vert = [0 : vcount-1], lat = [0 : zcount-1] ) {
            translate([hsize*horiz, vsize*vert, zsize*lat]) {
                cube([hsize-hmargin, vsize-vmargin, zsize-zmargin]);
			}
		}			
	}
}

// Bottom raised support
module raised_support(x, y, z) {
        translate([x, y, z])
            cylinder(d=support_diameter, h=thickness + 1 /* originally /2+1 */);
}

// Bottom screw hole
module bottom_screw_hole(x, y, z) {
    translate([x, y, z]) {
        cylinder(d=support_diameter, h=thickness/2);
        screw_hole();        
    }
}

module screw_hole() {
    cylinder(d=screw_diameter, h=screw_depth);
}
    
// Bottom
module bottom() {
    difference() {
        union() {
            difference() {
                minkowski() {
                    cylinder(r=2);
                    cube([width+2*overlay,height+2*overlay,thickness+2]);
                }

                // Recessed chamber for the board.
                translate([overlay-1, overlay-1, thickness - 0.5]) {
                    cube([width+2, height+2, 5]);
                }
            }

            // raised supports for the board.
            translate([0,0,thickness/2]) {
                for (x = [overlay+screw_margin, width+overlay-screw_margin],
                     y = [overlay+screw_margin, width+overlay-screw_margin] )
                    raised_support(x, y, 0);
            }
        }

        // Four screw holes
        for (x = [overlay+screw_margin, width+overlay-screw_margin],
             y = [overlay+screw_margin, width+overlay-screw_margin] )
            bottom_screw_hole(x, y, 0);
    }
}

module top_support(x, y, z) {
    translate([x, y, z]) {
        difference() {
            cylinder(d=support_diameter, h=depth+thickness);
            screw_hole();
        }
    }
}

// Top
module top() {
    translate([0,0,depth]) {
        difference() {
            minkowski() {
                cylinder(r=2);
                difference() {
                    cube([width+2*overlay,height+2*overlay,thickness]);
                    // Front panel
                    translate([overlay+6.2,0,0]) { 
                        cube([width-12.5,18,thickness]);
                    }
                    // Serial
                    translate([overlay-3,25,0]) { 
                        cube([11.5,33,thickness]);
                    }
                    // Logo
                    translate([overlay+9,24,0]) { 
                        cube([24,26,thickness]);
                    }
                    // ICSP
                    translate([overlay-2,70,0]) { 
                        cube([14,22,thickness]);
                    }

                    // SD Module bay
                    translate([overlay+10.1,height+overlay-26,0]) { 
                        cube([14,30.9,thickness]);
                    }
                    // RTC Module bay
                    translate([overlay+30.1,height+overlay-24,0]) { 
                        cube([21,28.1,thickness]);
                    }
                    // GPIO
                    translate([overlay+width-52,height+overlay-11 ,0]) { 
                        cube([46,12,thickness]); // all these were +2
                    }

                }

            }

            // slanted vents
            translate([25, 23, 0]) {
                rotate([-18, 0, 0]) {
                    #ventpunch(width/1.3, height/2, depth+10, 3, 3, 3, 4, 10, 1);
                }
            }
        }
            
        // Logo frame
        translate([overlay+7,24,0]) {
            difference() {
                cube([24,28,thickness+1]);
                translate([4,4,0]) {
                    cube([18,20,thickness+1]);
                }
            }
        }
    }

    // Four supports
    for (x = [overlay+screw_margin, width+overlay-screw_margin],
         y = [overlay+screw_margin, width+overlay-screw_margin])
      top_support(x, y, 0);  

}


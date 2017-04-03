; Example file illustrating an eigenmode source, generating a waveguide mode
; (requires recent MPB version to be installed before Meep is compiled)
; General template to calcule field transmition from the transmition source to an output volume
; Every space unit is in micro meters.

;; Don't think you must pass anything here;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define-param l 1.550                       )       ; Vacuum center source wavelenght
(define-param dl 0.120                      )       ; Target source wavelenght bandwich
;;(/ (/ (* l l) dl) (* 2 2048))                    )       ; Time resolution of the output field - take a look on Nyquist–Shannon sampling theorem -talk with Leandro



(define-param decay-by 0.01                 )       ; Criteria to end simulation. 0.01 is good enough
(define-param pml_thick  l             )       ; pml thickness. Its ok half wavelenght.
(define-param mode 1                        )       ; input source mode
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; The parameters you need to pass are the ones with create_geo.py arguments. Ex: ;;; (foo).
;; To pass use meep LX=10 LY=10 index_file="myfile.h5" template-meep.ctl

(define-param index_file "index.h5"         ) ;;; (INDEX_FILE) h5 input, usually made on create_geo.py 
(define-param field_file_append "field"     ) ;;; h5 output fields. These field should be used performe spectral analysis  
(define-param LX 20.0                       ) ;;; (LX) Computational size dimensions
(define-param LY 20.0                       ) ;;; (LY)
(define-param LZ no-size                    ) ;;; Just for the sake of future 3d
(define-param s_resol 0.050                 ) ;;; (RESOLUTION) Use the same as in create_geo.py. Not mandatory I think.

                            ;;; SOURCE POSITION. Left/button "xy" notation as in create_geo.py
(define-param sx (* 2 pml_thick)            ) ;;; (X_source=0) 
(define-param sy (/ LY 2)                   ) ;;; (Y_source)
(define-param sz (/ LZ 2)                   ) ;;; (Z_source)

                            ;;; Defining SOURCE VOLUME      
(define-param source-lx 0                   ) ;;; (LX_SOURCE=0)
(define-param source-ly 1.2                 ) ;;; (LY_SOURCE=1) The source must be slight bigger than the input waveguide.  
(define-param source-lz no-size             ) ;;; (LZ_SOURCE=no size)

                            ;;; OUTPUT POSITION. Left/button "xy" notation as in create_geo.py
(define-param ox (- LX pml_thick l)         ) ;;; (X_OUTPUT=LX) Same for output observation section
(define-param oy (/ LY 2)                   ) ;;; (Y_OUTPUT)
(define-param oz (/ LZ 2)                   ) ;;; (Z_OUTPUT) 
(define-param out-lx 0                      ) ;;; 
(define-param out-ly LY                     ) ;;; (LY_OUTPUT)
(define-param out-lz no-size                ) ;;; (LZ_OUTPUT)

;You do not need to read from here.

(define resol (/ 1 s_resol)       ) ; make that integer please
(define dt (* 0.5 s_resol )       ) ;;; FDTD time Resolution
(define f (/ 1 l)                 ) ; Central frequency
(define df (/ dl (* l l))) ; Frequency Band
(define source-x (- sx  (/ LX 2) )) ; Change from left/button to meep centered position references
(define source-y (- sy  (/ LY 2) ))
(define source-z (- sz  (/ LZ 2) ))
(define out-x (- ox  (/ LX 2) ))
(define out-y (- oy  (/ LY 2) ))
(define out-z (- oz  (/ LZ 2) ))

(set! epsilon-input-file index_file) ; input refractive indexes

(set! geometry-lattice (make lattice (size LX LY no-size))) ; Define comp. domain. In 3d add LZ

;;Source
(set! sources (append sources (list
               (make eigenmode-source
                 (src (make gaussian-src (frequency f) (fwidth df)  ))
		 (size source-lx source-ly source-lz)
                 (center source-x source-y source-z) 
		 (component ALL-COMPONENTS)
		 (eig-band mode)
;; 		 (eig-parity EVEN-Y) ;; To enforce some symmetrie
		 )))
)

                 
(set! pml-layers (list (make pml (thickness pml_thick)))) ; set pml

(set! resolution resol) ; set resolution

(set! output-single-precision? true)

(run-sources+  
    (stop-when-fields-decayed 50 Hy (vector3 out-x out-y out-z ) decay-by)  ;; arguments are time range, field component, position, decay by. Easy not? 
;;     (harminv Hz (vector3 out-x out-y out-z) f df)
    (to-appended field_file_append ;;append to file
        (at-every dt (in-volume (volume (center out-x out-y out-z) (size  out-lx out-ly out-lz ))  ;; at every dt in volume the fields
        output-hfield output-efield output-dfield )) ;; output fields in volume
    (to-appended "full-field" ;;append to file
        (at-every 50 output-hfield)) ;; output fields in domain
    )
)
(define time (meep-time))
(print "grepme " "Spacial Resolution " s_resol "\n" )
(print "grepme " "Time Sampling " dt "\n" )
(print "grepme " "Central Frequency " f "\n" )
(print "grepme " "Banwidth Frequency " df "\n" )
(define Df (/ (/ 1 dt) time) )
(print "grepme " "Frequency Resolution " Df "\n" )
(print "grepme " "Central Wavelength " l "\n" )
(print "grepme " "Banwidth Wavelength " dl "\n" )
(print "grepme " "Wavelength Resolution " (* Df l l) "\n" )
(print "grepme " "Total time " time "\n" )
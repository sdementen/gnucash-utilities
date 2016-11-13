;; -*-scheme-*-
;; this file is autogenerated by the gnucash-utilities gc_report command
;; do not edit it as it will be overwritten

(define-module (gnucash report {{ project.name }}))
(use-modules (gnucash main)) ;; FIXME: delete after we finish modularizing.
(use-modules (gnucash gnc-module))
(use-modules (gnucash app-utils))
(use-modules (gnucash gettext))
(gnc:module-load "gnucash/engine" 0)
(use-modules (gnucash core-utils))


;; 'debug is deprecated and unused since guile 2
(cond-expand
  (guile-2 )
  (else
    (debug-enable 'debug)))
(debug-enable 'backtrace)

(gnc:module-load "gnucash/report/report-system" 0)
(gnc:module-load "gnucash/html" 0) ;for gnc-build-url



;; This function will generate a set of options that GnuCash
;; will use to display a dialog where the user can select
;; values for your report's parameters.
(define (options-generator)    
  (let* ((options (gnc:new-options)) 
         ;; This is just a helper function for making options.
         ;; See gnucash/src/app-utils/options.scm for details.
         (add-option 
          (lambda (new-option)
            (gnc:register-option options new-option))))
    

    ;; This is a number range option. The user can enter a number
    ;; between a lower and upper bound given below. There are also
    ;; arrows the user can click to go up or down, the amount changed
    ;; by a single click is given by the step size.
    {% for option in project.options %}
    {{ option.render_scheme() }}
    {% endfor %}

    (gnc:options-set-default-section options "{{project.options_default_section}}")

    options))


(define (python-renderer report-obj)
  (define (get-op section name)
    (gnc:lookup-option (gnc:report-options report-obj) section name))
  (define (op-value section name)
    (gnc:option-value (get-op section name)))

  (let ((program '())
        (from-child #f)
        (to-child #f)
        )

    (define (start-program)
      (set! program (gnc-spawn-process-async
                     (list {{python_interpreter}} (gnc-build-dotgnucash-path "{{ project.python_script }}") "execute") ;; (gnc:session-get-url (gnc-get-current-session)))
                     #t)))

    (define (read-port port)
        (let iter ((result '()) (chr (read-char port)))
            (if (eof-object? chr)
                (list->string result)
                (iter (append result (list chr)) (read-char port)))))

    (define (get-sources)
          (let ((results #f))

            (set! to-child (fdes->outport (gnc-process-get-fd program 0)))
            (set! from-child (fdes->inport (gnc-process-get-fd program 1)))
            (catch
             #t
             (lambda ()

                {% for option in project.options %}
                (display "{{option.name}}"   to-child)
                (display "|"   to-child)
                (display {{ option.render_serialise() }}  to-child)

                (display "\n"   to-child)
                {% endfor %}

               (force-output to-child)
               (close-output-port to-child)
               (set! results (read-port from-child))
               results)
             (lambda (key . args)
               key))))

    (define (kill-program)
      (if (not (null? program))
          (gnc-detach-process program #t)))

    ;; (setenv "PYTHONPATH" "C:\\Users\\gfj138\\.gnucash")

    (dynamic-wind
        start-program
        get-sources
        kill-program)))


;; Here we define the actual report with gnc:define-report
(gnc:define-report
 
 ;; The version of this report.
 'version 1
 
 ;; The name of this report. This will be used, among other things,
 ;; for making its menu item in the main menu. You need to use the
 ;; untranslated value here!
 'name (N_ "{{project.title}}")

 ;; The GUID for this report. This string should be unique, set once
 ;; and left alone forever after that. In theory, you could use any
 ;; unique string, even a meaningful one (!) but its probably best to
 ;; use a true uuid. Get them from `uuidgen | sed -e s/-//g` and paste
 ;; the results in here. You must make a new guid for each report!
 'report-guid "{{project.guid}}"

 ;; The name in the menu
 ;; (only necessary if it differs from the name)
 ;; 'menu-name (N_ "Sample Report with Examples")

 ;; A tip that is used to provide additional information about the
 ;; report to the user.
 'menu-tip (N_ "{{project.menu_tip}}")

 ;; A path describing where to put the report in the menu system.
 ;; In this case, it's going under the utility menu.
 'menu-path (list gnc:menuname-utility)

 ;; The options generator function defined above.
 'options-generator options-generator
 
 ;; The rendering function defined above.
 'renderer python-renderer)

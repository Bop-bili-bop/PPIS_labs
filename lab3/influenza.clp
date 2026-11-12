; Лабораторная работа 3, вариант 6: «Грип».
; Учебная модель и демонстрация логического вывода, а не медицинский диагноз.

(defglobal
  ?*high-temperature* = 39.5
  ?*subfebrile-min* = 37.1
  ?*subfebrile-max* = 38.0)

(deftemplate session
  (slot educational-only (allowed-symbols yes no) (default yes)))

(deftemplate patient
  (slot id)
  (slot age-group (allowed-symbols child adult) (default adult)))

(deftemplate symptom
  (slot patient)
  (slot name)
  (slot present (allowed-symbols yes no) (default yes)))

(deftemplate temperature
  (slot patient)
  (slot degrees (type NUMBER))
  (slot fever-days (type INTEGER) (default 0)))

(deftemplate evidence
  (slot patient)
  (slot kind)
  (slot explanation))

(deftemplate severity
  (slot patient)
  (slot level (allowed-symbols mild marked severe)))

(deftemplate diagnostic-result
  (slot patient)
  (slot conclusion
    (allowed-symbols consistent-with-influenza-model
                     mild-influenza-like-presentation
                     insufficient-evidence))
  (slot explanation))

; deffacts creates only permanent model metadata. Scenario facts are selected
; independently by load-scenario, so demonstrations cannot contaminate each other.
(deffacts initial-model-state
  (session (educational-only yes)))

(deffunction temperature-band (?degrees)
  (if (>= ?degrees ?*high-temperature*) then
    (return very-high))
  (if (and (>= ?degrees ?*subfebrile-min*)
           (< ?degrees ?*subfebrile-max*)) then
    (return subfebrile))
  (if (>= ?degrees ?*subfebrile-max*) then
    (return elevated))
  (return normal))

(deffunction clear-case ()
  (do-for-all-facts ((?f patient)) TRUE (retract ?f))
  (do-for-all-facts ((?f symptom)) TRUE (retract ?f))
  (do-for-all-facts ((?f temperature)) TRUE (retract ?f))
  (do-for-all-facts ((?f evidence)) TRUE (retract ?f))
  (do-for-all-facts ((?f severity)) TRUE (retract ?f))
  (do-for-all-facts ((?f diagnostic-result)) TRUE (retract ?f)))

(deffunction load-scenario (?scenario)
  (clear-case)
  (if (eq ?scenario strong) then
    (assert (patient (id anna) (age-group adult)))
    (assert (temperature (patient anna) (degrees 39.7) (fever-days 3)))
    (assert (symptom (patient anna) (name acute-onset)))
    (assert (symptom (patient anna) (name chills)))
    (assert (symptom (patient anna) (name headache)))
    (assert (symptom (patient anna) (name frontal-headache)))
    (assert (symptom (patient anna) (name eye-movement-worsens-headache)))
    (assert (symptom (patient anna) (name general-weakness)))
    (assert (symptom (patient anna) (name muscle-pain)))
    (assert (symptom (patient anna) (name photophobia))))
  (if (eq ?scenario mild) then
    (assert (patient (id boris) (age-group adult)))
    (assert (temperature (patient boris) (degrees 37.6) (fever-days 2)))
    (assert (symptom (patient boris) (name acute-onset)))
    (assert (symptom (patient boris) (name headache)))
    (assert (symptom (patient boris) (name general-weakness)))
    (assert (symptom (patient boris) (name body-aches))))
  (if (eq ?scenario insufficient) then
    (assert (patient (id vera) (age-group adult)))
    (assert (temperature (patient vera) (degrees 36.7) (fever-days 0)))
    (assert (symptom (patient vera) (name tearing)))))

(deffunction show-result ()
  (do-for-all-facts ((?r diagnostic-result)) TRUE
    (printout t "Final result for " ?r:patient ": " ?r:conclusion crlf
                "Reason: " ?r:explanation crlf)))

(deffunction run-scenario (?scenario)
  (reset)
  (load-scenario ?scenario)
  (printout t crlf "=== Scenario: " ?scenario " ===" crlf)
  (facts)
  (run)
  (show-result))

; Intermediate evidence is completed before choosing a conclusion.
(defrule classify-temperature
  (declare (salience 50))
  (temperature (patient ?p) (degrees ?degrees) (fever-days ?days))
  =>
  (assert (evidence (patient ?p) (kind temperature-classified)
                    (explanation (temperature-band ?degrees))))
  (if (and (>= ?days 2) (<= ?days 6)) then
    (assert (evidence (patient ?p) (kind typical-fever-duration)
                      (explanation two-to-six-days)))))

(defrule systemic-aches
  (declare (salience 50))
  (symptom (patient ?p) (name general-weakness) (present yes))
  (or (symptom (patient ?p) (name muscle-pain) (present yes))
      (symptom (patient ?p) (name joint-pain) (present yes))
      (symptom (patient ?p) (name body-aches) (present yes)))
  =>
  (assert (evidence (patient ?p) (kind systemic-aches)
                    (explanation weakness-and-aches))))

(defrule characteristic-headache
  (declare (salience 50))
  (or (symptom (patient ?p) (name frontal-headache) (present yes))
      (symptom (patient ?p) (name pain-behind-eyes) (present yes)))
  (symptom (patient ?p) (name eye-movement-worsens-headache) (present yes))
  =>
  (assert (evidence (patient ?p) (kind characteristic-headache)
                    (explanation eye-movement-worsens-localized-headache))))

(defrule strong-model-match
  (declare (salience 30))
  (patient (id ?p))
  (symptom (patient ?p) (name acute-onset) (present yes))
  (temperature (patient ?p) (degrees ?t&:(>= ?t ?*subfebrile-min*)))
  (symptom (patient ?p) (name general-weakness) (present yes))
  (or (and (symptom (patient ?p) (name chills) (present yes))
           (evidence (patient ?p) (kind systemic-aches)))
      (evidence (patient ?p) (kind characteristic-headache)))
  (not (diagnostic-result (patient ?p)))
  =>
  (assert (diagnostic-result (patient ?p)
            (conclusion consistent-with-influenza-model)
            (explanation acute-fever-and-characteristic-pattern))))

(defrule mild-model-match
  (declare (salience 20))
  (patient (id ?p))
  (symptom (patient ?p) (name acute-onset) (present yes))
  (temperature (patient ?p) (degrees ?t&:(and (>= ?t ?*subfebrile-min*)
                                              (< ?t ?*subfebrile-max*))))
  (symptom (patient ?p) (name general-weakness) (present yes))
  (or (symptom (patient ?p) (name headache) (present yes))
      (symptom (patient ?p) (name body-aches) (present yes)))
  (not (diagnostic-result (patient ?p)))
  =>
  (assert (diagnostic-result (patient ?p)
            (conclusion mild-influenza-like-presentation)
            (explanation acute-subfebrile-weakness-with-headache-or-body-aches))))

(defrule severe-neurological-signs
  (declare (salience 10))
  (temperature (patient ?p) (degrees ?t&:(>= ?t ?*high-temperature*)))
  (or (symptom (patient ?p) (name vomiting) (present yes))
      (symptom (patient ?p) (name hallucinations) (present yes))
      (symptom (patient ?p) (name nervous-system-symptom) (present yes))
      (symptom (patient ?p) (name seizures) (present yes)))
  (not (severity (patient ?p)))
  =>
  (assert (severity (patient ?p) (level severe))))

(defrule marked-systemic-presentation
  (declare (salience 5))
  (temperature (patient ?p) (degrees ?t&:(>= ?t ?*high-temperature*)))
  (evidence (patient ?p) (kind systemic-aches))
  (not (severity (patient ?p)))
  =>
  (assert (severity (patient ?p) (level marked))))

(defrule mild-temperature
  (temperature (patient ?p) (degrees ?t&:(and (>= ?t ?*subfebrile-min*)
                                              (< ?t ?*subfebrile-max*))))
  (not (severity (patient ?p)))
  =>
  (assert (severity (patient ?p) (level mild))))

(defrule insufficient-evidence
  (declare (salience -100))
  (patient (id ?p))
  (not (diagnostic-result (patient ?p)))
  =>
  (assert (diagnostic-result (patient ?p)
            (conclusion insufficient-evidence)
            (explanation criteria-of-the-educational-model-not-met))))

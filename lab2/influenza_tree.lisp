;;;; Laboratory work 2, variant 6: "Influenza"
;;;; Educational decision tree only; it is not a medical diagnostic tool.

(defpackage :influenza-tree
  (:use :cl)
  (:export :*influenza-tree* :diagnose-interactively :diagnose-with-answers
           :run-test-scenarios))

(in-package :influenza-tree)

(defstruct question
  "A binary decision-tree node. YES-BRANCH and NO-BRANCH are nodes or leaves."
  id
  prompt
  yes-branch
  no-branch)

(defstruct conclusion
  "An educational conclusion stored in a leaf of the tree."
  id
  label
  explanation)

(defparameter *consistent*
  (make-conclusion
   :id :consistent
   :label "Symptoms are consistent with the influenza knowledge model"
   :explanation
   "The combination includes acute onset, fever and several characteristic early/systemic findings."))

(defparameter *mild*
  (make-conclusion
   :id :mild
   :label "Mild influenza-like presentation"
   :explanation
   "Acute onset and a mild fever occur together with headache, weakness and body or muscle aches."))

(defparameter *insufficient*
  (make-conclusion
   :id :insufficient
   :label "Insufficient evidence"
   :explanation
   "The supplied answers do not form one of the influenza patterns represented by this educational tree."))

;; Leaves and subtrees are shared deliberately: the representation is a binary
;; decision graph, while every traversal still follows a single tree-shaped path.
(defparameter *influenza-tree*
  (make-question
   :id :acute-onset
   :prompt "Did the symptoms begin acutely?"
   :no-branch *insufficient*
   :yes-branch
   (make-question
    :id :elevated-temperature
    :prompt "Is body temperature elevated?"
    :no-branch *insufficient*
    :yes-branch
    (make-question
     :id :very-high-temperature
     :prompt "Is the temperature very high (rapidly rising toward 40 C)?"
     :yes-branch
     (make-question
      :id :chills
      :prompt "Are chills present?"
      :yes-branch
      (make-question
       :id :headache
       :prompt "Is headache present?"
       :yes-branch *consistent*
       :no-branch *insufficient*)
      :no-branch
      (make-question
       :id :headache
       :prompt "Is headache present?"
       :no-branch *insufficient*
       :yes-branch
       (make-question
        :id :general-weakness
        :prompt "Is general weakness present?"
        :yes-branch *consistent*
        :no-branch *insufficient*)))
     :no-branch
     (make-question
      :id :headache
      :prompt "Is headache present?"
      :no-branch *insufficient*
      :yes-branch
      (make-question
       :id :general-weakness
       :prompt "Is general weakness present?"
       :no-branch *insufficient*
       :yes-branch
       (make-question
        :id :muscle-or-body-aches
        :prompt "Are muscle pain or body aches present?"
        :yes-branch *mild*
        :no-branch *insufficient*)))))))

(defun ask-yes-no (prompt &optional (input *standard-input*)
                                    (output *standard-output*))
  "Ask PROMPT until the user enters yes/y or no/n, then return a Boolean."
  (loop
    (format output "~A [yes/no]: " prompt)
    (finish-output output)
    (let ((answer (read-line input nil nil)))
      (when (null answer)
        (error "End of input while waiting for a yes/no answer."))
      (cond ((member (string-downcase (string-trim '(#\Space #\Tab) answer))
                     '("yes" "y") :test #'string=)
             (return t))
            ((member (string-downcase (string-trim '(#\Space #\Tab) answer))
                     '("no" "n") :test #'string=)
             (return nil))
            (t (format output "Please answer yes or no.~%"))))))

(defun traverse-tree (node answer-provider)
  "Recursively traverse NODE, obtaining Booleans from ANSWER-PROVIDER."
  (etypecase node
    (conclusion node)
    (question
     (traverse-tree
      (if (funcall answer-provider node)
          (question-yes-branch node)
          (question-no-branch node))
      answer-provider))))

(defun print-conclusion (result &optional (stream *standard-output*))
  (format stream "~%Result: ~A~%Reason: ~A~%~%Educational prototype only; this is not a medical diagnosis.~%"
          (conclusion-label result)
          (conclusion-explanation result))
  result)

(defun diagnose-interactively ()
  "Traverse the influenza tree interactively and print its educational result."
  (print-conclusion
   (traverse-tree *influenza-tree*
                  (lambda (node) (ask-yes-no (question-prompt node))))))

(defun diagnose-with-answers (answers)
  "Deterministically traverse the tree using an alist of (:QUESTION-ID . BOOLEAN).

Only questions reached on the selected path need answers. A missing answer is
reported as an error, which makes scenarios reproducible and prevents an
unknown observation from being silently interpreted as NO."
  (traverse-tree
   *influenza-tree*
   (lambda (node)
     (let ((entry (assoc (question-id node) answers)))
       (unless entry
         (error "No deterministic answer supplied for ~S." (question-id node)))
       (not (null (cdr entry)))))))

(defparameter *test-scenarios*
  (list
   (list :name "strong influenza pattern"
         :answers '((:acute-onset . t) (:elevated-temperature . t)
                    (:very-high-temperature . t) (:chills . t)
                    (:headache . t))
         :expected :consistent)
   (list :name "mild influenza-like pattern"
         :answers '((:acute-onset . t) (:elevated-temperature . t)
                    (:very-high-temperature . nil) (:headache . t)
                    (:general-weakness . t) (:muscle-or-body-aches . t))
         :expected :mild)
   (list :name "insufficient evidence"
         :answers '((:acute-onset . nil))
         :expected :insufficient)))

(defun run-test-scenarios (&optional (stream *standard-output*))
  "Run and assert the three deterministic demonstration scenarios."
  (dolist (scenario *test-scenarios* t)
    (let* ((result (diagnose-with-answers (getf scenario :answers)))
           (actual (conclusion-id result))
           (expected (getf scenario :expected)))
      (format stream "~A: ~A (~A)~%"
              (getf scenario :name) (conclusion-label result)
              (if (eql actual expected) "PASS" "FAIL"))
      (assert (eql actual expected) ()
              "Scenario ~A expected ~S but got ~S."
              (getf scenario :name) expected actual))))


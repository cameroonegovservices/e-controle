<template>
  <div>
    <questionnaire-metadata-create
            ref="createMetadataChild"
            v-on:metadata-created="metadataCreated"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-on:body-created="bodyCreated"
            v-on:back="back"
            v-show="state === STATES.CREATING_BODY">
    </questionnaire-body-create>
    <questionnaire-preview
            ref="previewChild"
            v-on:back="back"
            v-show="state === STATES.PREVIEW">
    </questionnaire-preview>
  </div>
</template>

<script>
  import Vue from "vue";
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"
  import QuestionnairePreview from "./QuestionnairePreview";

  // State machine
  let STATES = {
    START : "start",
    // Transition : metadata-created / back
    CREATING_BODY : "creating_body",
    // Transition : body-created / back
    PREVIEW: "preview"
  };

  export default Vue.extend({
    data() {
      return {
        STATES : STATES,
        questionnaire: {},
        state: STATES.START
      }
    },
    methods: {
    },
    components: {
      QuestionnaireBodyCreate,
      QuestionnaireMetadataCreate,
      QuestionnairePreview
    },
    mounted() {
      this.emitQuestionnaireUpdated();
    },
    methods: {
      emitQuestionnaireUpdated: function() {
        this.$emit('questionnaire-updated', this.questionnaire);
      },
      moveToState: function(newState) {
        this.state = newState;
      },
      bodyCreated: function(data) {
        console.log('got body', data);
        // "this" is the child component.
        this.questionnaire.body = data;
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.PREVIEW);
      },
      metadataCreated: function(data) {
        console.log('got metadata', data);
        // "this" is the child component.
        this.questionnaire.metadata = data;
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.CREATING_BODY);
      },
      back: function() {
        console.log('back');
        if (this.state === STATES.CREATING_BODY) {
          this.moveToState(STATES.START);
          return;
        }
        if (this.state === STATES.PREVIEW) {
          this.moveToState(STATES.CREATING_BODY)
          return;
        }
        console.error('Trying to go back from state', this.state);
      }
    }
  });
</script>

<style></style>

<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" fill-height color="#f5efe6">
          <v-btn to="/photo" text class="ml-5 mt-5"> - 요리 사진 게시판</v-btn>
          <v-row>
              <v-col>
                <v-card fill-height color="#f5efe6" class="mt-10" flat>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <v-card-title primary-title style="color:#7895B2">
                          작성자
                        </v-card-title>
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 이름 넣어주세요 -->
                        <v-card-title primary-title >
                          {{nickname}}
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat style="color:#7895B2">
                        <v-card-title>
                          작성일
                        </v-card-title>
                        
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 날짜 넣어주세요 -->
                        <v-card-title primary-title>
                          {{upload_time}}
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
          </v-row>
          
          <v-row >
            <v-col justify="center">
              <v-card v-if="preview" >
                <v-img :src="preview" class="img-fluid" contain/>
              </v-card>
              <input type="file" accept="image/*" @change="previewImage" class="form-control-file" id="my-file">
            </v-col>
          </v-row>

          <v-card height="300" color="#f5efe6" flat id="card-on-off">
          </v-card>

          <v-row>
            <v-col offset="5" col="2">
              <v-btn x-large color="#7895B2" @click="addPhoto">게시글 게시</v-btn>
            </v-col>
          </v-row>

        </v-card>
      </v-col>
    </v-row>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        headerTitle = "게시글 등록 오류"
        btn1Title="확인"
        :btn2=false
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>게시글 등록에 실패했습니다.</div>
        </template>
      </popup-dialog>
    </v-dialog>

  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import PopupDialog from '@/components/popup.vue';
import router from '@/router';

export default{
  components: {
    PopupDialog
  },
  data(){
    return {
      popupDialog: false,
      preview: null,
      image: null,
      nickname: "",
      upload_time: ""
    };
  },
  mounted(){
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.nickname = UserInfo.nickname;
    const date = new Date();
    this.upload_time = date.toLocaleString('ko-kr');
  },
  methods: {
    showDialog() { // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false
    },
    previewImage: function(event) {
      const btn1 = document.getElementById('card-on-off')
      if(btn1.style.display !== 'none') {
        btn1.style.display = 'none';
      }

      var input = event.target;
      if (input.files) {
        var reader = new FileReader();
        reader.onload = (e) => {
          this.preview = e.target.result;
          this.image = this.preview;
        }
        this.image=input.files[0];
        reader.readAsDataURL(input.files[0]);
      }
    },
    reset: function() {
      this.image = null;
      this.preview = null;
      this.image_list = [];
      this.preview_list = [];
    },

    addPhoto() {
      const newPhoto = JSON.stringify (
        {
	        "post_id": null,
          "photo_link": this.image.split(/[\,]/)[1],
          "like_count":0,
          "upload_time": null,
          "nickname":this.nickname
        }
      );
      
      herokuAPI.photoAdd(newPhoto) 
        .then(function (response) {
          console.log("전송 정보",  newPhoto);
          if(response.status == 200) {
            console.log("응답 정보", response.data);
            router.push({path: "/photo"});
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB error");
            vm.showDialog();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.showDialog();
          }
        });
    }
  }
}

</script>
<template>
  <v-container>
    <v-layout>
      <v-row justify="center">
        <v-col cols="8">
          <v-card min-height="800" color="#f5efe6">
            <v-card-title id="title1" class="pt-16 pl-16 pb-10">
              냉장고
            </v-card-title>
            <v-layout>
              <v-row justify="center">
                <v-col cols="10">
                  <v-card class="mb-5">
                    <v-row justify="space-between">
                      <v-card-title id="title2" class="pl-10">
                        보유 재료
                      </v-card-title>
                      <v-btn color="#7895b2" dark class="mt-4 mr-10" @click="showAddIngredientDialog">재료추가</v-btn>
                    </v-row>

                    <!-- 재료 없는 경우 -->
                    <v-card-text v-if="isEmpty">보유 재료가 없습니다.</v-card-text>
                  
                    <!-- 재료 있는 경우 -->
                    <v-card-text v-if="!isEmpty">
                      <!-- 재료 v card -->
                      <div v-for="item in refrigerators" :key="item.id" class="ingre-card">
                        <!-- 7일 이상 남음 -->
                        <div v-if="item.expireDate > 7 && item.expireDate != null" class="ingre-green">
                          <!-- 7일 이상 남은 재료 -->
                          <div class="d-flex justify-space-between">
                            <span class="ml-3 my-2" style="font-size:1.8em">{{item.name}}</span>
                            <span class="mr-3 my-2" style="font-size:1.8em">{{item.amount}}{{item.unit}}</span>
                          </div>

                          <!-- 구분선 -->
                          <v-divider />

                          <!-- 아랫줄 -->
                          <div class="d-flex justify-space-between align-center">
                            <span class="ml-3" style="font-size:1.2em">{{item.expiry_date}}</span>
                            <div class="mr-3">
                              <v-btn small color="#AEBDCA" class="my-2" @click="beforeEdit(item)">수정하기</v-btn>
                              <v-btn small color="#AEBDCA" class="ml-3 my-2" @click="deletePopup(item.id)">삭제하기</v-btn>
                            </div>
                          </div>
                        </div>
                        <!-- 3~7일 남음 -->
                        <div v-if="item.expireDate > 3 && item.expireDate <= 7 && item.expireDate != null" class="ingre-yellow">
                          <!-- 7일 이상 남은 재료 -->
                          <div class="d-flex justify-space-between">
                            <span class="ml-3 my-2" style="font-size:1.8em">{{item.name}}</span>
                            <span class="mr-3 my-2" style="font-size:1.8em">{{item.amount}}{{item.unit}}</span>
                          </div>

                          <!-- 구분선 -->
                          <v-divider />

                          <!-- 아랫줄 -->
                          <div class="d-flex justify-space-between align-center">
                            <span class="ml-3" style="font-size:1.2em">{{item.expiry_date}}</span>
                            <div class="mr-3">
                              <v-btn small color="#AEBDCA" class="my-2" @click="beforeEdit(item)">수정하기</v-btn>
                              <v-btn small color="#AEBDCA" class="ml-3 my-2" @click="deletePopup(item.id)">삭제하기</v-btn>
                            </div>
                          </div>
                        </div>
                        <!-- 0~3일 남음 -->
                        <div v-if="item.expireDate >= 0 && item.expireDate <= 3 && item.expireDate != null" class="ingre-red">
                          <!-- 7일 이상 남은 재료 -->
                          <div class="d-flex justify-space-between">
                            <span class="ml-3 my-2" style="font-size:1.8em">{{item.name}}</span>
                            <span class="mr-3 my-2" style="font-size:1.8em">{{item.amount}}{{item.unit}}</span>
                          </div>

                          <!-- 구분선 -->
                          <v-divider />

                          <!-- 아랫줄 -->
                          <div class="d-flex justify-space-between align-center">
                            <span class="ml-3" style="font-size:1.2em">{{item.expiry_date}}</span>
                            <div class="mr-3">
                              <v-btn small color="#AEBDCA" class="my-2" @click="beforeEdit(item)">수정하기</v-btn>
                              <v-btn small color="#AEBDCA" class="ml-3 my-2" @click="deletePopup(item.id)">삭제하기</v-btn>
                            </div>
                          </div>
                        </div>
                        <!-- 유통기한 지남 -->
                        <div v-if="item.expireDate < 0 && item.expireDate != null" class="ingre-black">
                          <!-- 7일 이상 남은 재료 -->
                          <div class="d-flex justify-space-between">
                            <span class="ml-3 my-2" style="font-size:1.8em">{{item.name}}</span>
                            <span class="mr-3 my-2" style="font-size:1.8em">{{item.amount}}{{item.unit}}</span>
                          </div>

                          <!-- 구분선 -->
                          <v-divider />

                          <!-- 아랫줄 -->
                          <div class="d-flex justify-space-between align-center">
                            <span class="ml-3" style="font-size:1.2em">{{item.expiry_date}}</span>
                            <div class="mr-3">
                              <v-btn small color="#AEBDCA" class="my-2" @click="beforeEdit(item)">수정하기</v-btn>
                              <v-btn small color="#AEBDCA" class="ml-3 my-2" @click="deletePopup(item.id)">삭제하기</v-btn>
                            </div>
                          </div>
                        </div>
                        <!-- 유통기한 없음 -->
                        <div v-if="item.expireDate == null">
                          <!-- 7일 이상 남은 재료 -->
                          <div class="d-flex justify-space-between">
                            <span class="ml-3 my-2" style="font-size:1.8em">{{item.name}}</span>
                            <span class="mr-3 my-2" style="font-size:1.8em">{{item.amount}}{{item.unit}}</span>
                          </div>

                          <!-- 구분선 -->
                          <v-divider />

                          <!-- 아랫줄 -->
                          <div class="d-flex justify-space-between align-center">
                            <span class="ml-3" style="font-size:1.2em">{{item.expiry_date}}</span>
                            <div class="mr-3">
                              <v-btn small color="#AEBDCA" class="my-2" @click="beforeEdit(item)">수정하기</v-btn>
                              <v-btn small color="#AEBDCA" class="ml-3 my-2" @click="deletePopup(item.id)">삭제하기</v-btn>
                            </div>
                          </div>
                        </div>
                        
                      </div>
                    </v-card-text>
                    
                  </v-card>
                </v-col>
              </v-row>  
            </v-layout>
          </v-card>
        </v-col>
      </v-row>
    </v-layout>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=headerTitle
        :btn1Title=btn1Title
        :btn2Title=btn2Title
        :btn2=btn2
        @hide="hideDialog"
        @submit="deleteIngre"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>{{ content1 }}</div>
        </template>
      </popup-dialog>
    </v-dialog>

    <!-- 재료 추가 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="addIngredientDialog"
    >
      <add-ingredient-dialog
        @update="update"
        @hide="hideAddIngredientDialog"
      />
    </v-dialog>

    <!-- 재료 수정 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="editIngredientDialog"
    >
      <edit-ingredient-dialog
        :idP="id"
        :nameP="name"
        :amountP="amount"
        :unitP="unit"
        @update="update"
        @hide="hideEditIngredientDialog"
      />
    </v-dialog>

  </v-container>
</template>

// Pagination

<script>
import herokuAPI from '@/api/heroku.js';
import PopupDialog from '@/components/popup.vue';
import AddIngredientDialog from '@/components/addIngredient.vue';
import EditIngredientDialog from '@/components/editIngredient.vue';

export default{
  components: {
    PopupDialog,
    AddIngredientDialog,
    EditIngredientDialog
  },
  data(){
    return{
      popupDialog: false,
      headerTitle: "",
      content1: "",
      btn1Title: "",
      btn2Title: "",
      btn2: false,
      id: -1,
      name: "",
      amount: -1,
      unit: "",
      addIngredientDialog: false,
      editIngredientDialog: false,
      refrigerators: [],
      isEmpty: false,

      //현재 날짜를 저장하는 변수
      todayDate : null,
    }
  },
  mounted() {
    // 냉장고 조회
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    let vm = this;

    // 현재 날짜 저장하는 코드
    let now = new Date();
    console.log(now);

    herokuAPI.refrigeratorLookup(UserInfo.nickname)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data[i] != null; i++) {
              if(response.data[i].expiry_date != null){
                var temp = new Date(response.data[i].expiry_date);
                response.data[i].expireDate = Math.ceil((temp-now)/(1000*60*60*24));
              } else {
                response.data[i].expireDate = null;
              }
              
              vm.refrigerators.push(response.data[i]);
            }
          }
      })
      .catch(function (e) {
        if(e.response.status == 401) {
          console.log("조회 실패");
          vm.requestFailPopup();
        } else if(e.response.status == 404) {
          console.log("404 식재료 없음");
          vm.isEmpty = true;
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.requestFailPopup();
        }
      });
  },
  methods: {
  // 팝업창 메소드들
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    deletePopup(click_id) {
      this.headerTitle = "재료 삭제";
      this.content1 = "해당 식재료를 삭제하시겠습니까?";
      this.btn1Title = "취소";
      this.btn2Title = "삭제";
      this.btn2 = true;
      this.id = click_id;
      this.showDialog();
    },
    deleteFailPopup() {
      this.headerTitle = "재료 삭제 실패";
      this.content1 = "재료 삭제에 실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    requestFailPopup() {
      this.headerTitle = "보유 재료 불러오기 실패";
      this.content1 = "보유 재료 조회에 실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    deleteIngre() {
      let vm = this;
      const deleteTarget = JSON.stringify ({ "id": this.id });
      herokuAPI.refrigeratorDelete(deleteTarget)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("삭제 성공");
            vm.$router.go();
          }
        })
        .catch(function (e) {
        if(e.response.status == 406) {
          console.log("406 삭제 실패");
          vm.deleteFailPopup();
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.deleteFailPopup();
        }
      });
    },

  // 재료추가 팝업창 메소드들
    showAddIngredientDialog() {
      this.addIngredientDialog = true;
    },
    hideAddIngredientDialog() {
      this.addIngredientDialog = false;
    },
  // 재료수정 팝업창 메소드들
    showEditIngredientDialog() {
      this.editIngredientDialog = true;
    },
    hideEditIngredientDialog() {
      this.editIngredientDialog = false;
    },
    beforeEdit(object) {
      this.id = object.id;
      this.name = object.name;
      this.amount = object.amount;
      this.unit = object.unit;
      this.showEditIngredientDialog();
    },
    update() {
      this.$router.go();
    },
  }
}
</script>

<style>
  #title1{
    font-size: 2em;
    color: #7895b2;
  }
  #title2{
    font-size: 1.4em;
    color: #7895b2;
  }

  .ingre-card {
    border: 1px solid rgb(182, 182, 182);
    border-radius: 10px;
    margin-top: 10px;
  }

  .ingre-green {
    background-color: rgb(93, 232, 93);
    border-radius: 9px;
  }

  .ingre-yellow {
    background-color: rgb(255, 255, 117);
    border-radius: 9px;
  }

  .ingre-red {
    background-color: rgb(255, 161, 161);
    border-radius: 9px;
  }

  .ingre-black {
    background-color: rgb(179, 179, 179);
    border-radius: 9px;
  }

</style>
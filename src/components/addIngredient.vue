<template>
  <v-card>
    <!-- 재료 입력 부분 -->
    <v-card-text>

      <div style="color:#7895B2; font-size: 2.1em;" class="py-6">
        보유 재료 추가
      </div>

      <div style="color:#7895B2; font-size: 1.3em;">
        추가할 재료 선택
      </div>

      <div class="searchbox mb-6">
        <div class="header">
          <v-text-field
            placeholder="추가할 재료 입력"
            hide-details="auto"
            id="inputText"
            @keyup="ingredient_filter"
            class="mx-6"
            v-model="name"
          ></v-text-field>
        </div>
  
        <div class="ingredient-container mx-6">
          <div v-for="i in ingredients" :key="i.name">
            <span ref="ingreName" class="ingreName visible" @click="clickIngredient">{{i.name}}</span>
          </div>
        </div>
      </div>
      
      <div style="color:#7895B2; font-size: 1.3em;">
        수량
      </div>

      <v-text-field
        placeholder="수량 입력"
        hide-details="auto"
        id="inputText"
        class="mx-6 mb-8"
        v-model="amount"
      ></v-text-field>

      <div style="color:#7895B2; font-size: 1.3em;">
        단위
      </div>

      <v-text-field
        placeholder="단위 입력"
        id="inputUnit"
        @click="units_filter"
        class="mx-6 mb-0"
      ></v-text-field>

      <div class="units-container mx-6">
        <div v-for="i in units" :key="i.name">
          <span ref="unitsName" class="unitsName visible" @click="clickUnit">{{i.name}}</span>
        </div>
        <div class="mb-13"></div>
      </div>

      <div style="color:#7895B2; font-size: 1.3em;">
        유통기한
      </div>

      <v-date-picker 
        v-model="expiry_date" 
        :show-current="true" 
        :landscape="true" 
        :reactive="true"
        color="#7895B2"
        class=""
      >
      </v-date-picker>      

      <div class="d-flex justify-center">
         <v-checkbox label="유통기한 선택 안함" v-model="is_expiry_not_exist"></v-checkbox>
      </div>
     
      
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center">
      <v-btn
        color="#7895B2"
        x-large
        @click="addIngre()"
      >
        추가하기
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style>

.searchbox{
  overflow: hidden;
}

.ingredient-container{
  max-height:100px;
  overflow: scroll;
}

.units-container{
  overflow: auto;
}

.ingreName{
  display: none;
  cursor: pointer;
}

.unitsName{
  display: none;
  cursor: pointer;
}

.visible{
  display: flex;
}

</style>

<script>
import herokuAPI from '@/api/heroku.js';
const Hangul = require('hangul-js');

export default{
  name: "addIngredient",
  data() {
    return {
      name: "",
      amount: "",
      unit: "",
      expiry_date: null,
      nickname: "",

      // 검색 목록
      ingredients : [
        {name: "가리비"},
        {name: "갈치"},
        {name: "감자"},
        {name: "계란"},
        {name: "고구마"},
        {name: "고등어"},
        {name: "고추"},
        {name: "고추장"},
        {name: "국간장"},
        {name: "굴"},
        {name: "굴소스"},
        {name: "김치"},
        {name: "깨"},
        {name: "깻잎"},
        {name: "꼬막"},
        {name: "꽁치"},
        {name: "꽃게"},
        {name: "낙지"},
        {name: "냉이"},
        {name: "느타리버섯"},
        {name: "다시다"},
        {name: "다시마"},
        {name: "달래"},
        {name: "닭고기"},
        {name: "당근"},
        {name: "대구"},
        {name: "대추"},
        {name: "대파"},
        {name: "돔베기"},
        {name: "돼지고기"},
        {name: "된장"},
        {name: "두부"},
        {name: "마늘"},
        {name: "마늘쫑"},
        {name: "마요네즈"},
        {name: "맥주"},
        {name: "메추리알"},
        {name: "멸치"},
        {name: "멸치액젓"},
        {name: "명이나물"},
        {name: "명태"},
        {name: "무"},
        {name: "문어"},
        {name: "물"},
        {name: "미더덕"},
        {name: "미역"},
        {name: "밀가루"},
        {name: "바지락"},
        {name: "밤"},
        {name: "버터"},
        {name: "부추"},
        {name: "빵"},
        {name: "상추"},
        {name: "새송이버섯"},
        {name: "새우"},
        {name: "새우젓"},
        {name: "설탕"},
        {name: "소고기"},
        {name: "소금"},
        {name: "소라"},
        {name: "소세지"},
        {name: "순두부"},
        {name: "시금치"},
        {name: "시래기"},
        {name: "쌀"},
        {name: "아스파라거스"},
        {name: "애호박"},
        {name: "양고기"},
        {name: "양배추"},
        {name: "양상추"},
        {name: "양파"},
        {name: "연어"},
        {name: "오리고기"},
        {name: "오징어"},
        {name: "옥수수"},
        {name: "우유"},
        {name: "잼"},
        {name: "전복"},
        {name: "진간장"},
        {name: "쪽파"},
        {name: "쭈꾸미"},
        {name: "참기름"},
        {name: "참나물"},
        {name: "청양고추"},
        {name: "청주"},
        {name: "치즈"},
        {name: "케챱"},
        {name: "콩"},
        {name: "키조개"},
        {name: "토마토"},
        {name: "팥"},
        {name: "팽이버섯"},
        {name: "표고버섯"},
        {name: "햄"},
        {name: "현미"},
        {name: "호박"},
        {name: "홍어"},
        {name: "홍합"},
        {name: "후추"},
        {name: "흑미"}
      ],

      // 단위 목록
      units : [
        {name : "g"},
        {name : "kg"},
        {name : "l"},
        {name : "ml"},
        {name : "T"},
      ],

      // 단위 선택시를 위한 변수
      unitLabel : "단위 입력",
      
      // 유통기한 선택 안함을 위한 변수
      is_expiry_not_exist : false,
    };
  },
  props: {
    isRecipe: {
      type: Boolean,
      default: false,
    },
  },
  mounted(){
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.nickname = UserInfo.nickname;

    // 동적 검색 설정
    for (var i=0;i<this.ingredients.length;i++){
      this.$refs.ingreName[i].classList.remove('visible');
    }
    for (var i=0;i<this.units.length;i++){
      this.$refs.unitsName[i].classList.remove('visible');
    }
    
  },
  methods: {
    addIngre() {
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const Ingre = {
          "amount": vm.amount,
          "expiry_date": this.is_expiry_not_exist ? null : vm.expiry_date, // 없어도 됨
          "name" : vm.name,
          "nickname" : UserInfo.nickname,
          "unit" : vm.unit,
        };
      if(vm.isRecipe == true) {
        vm.$emit('hide');
        vm.$emit('add', Ingre);
      } else {
        const AddIngre = JSON.stringify (Ingre);
        console.log(AddIngre);
        herokuAPI.refrigeratorAdd(AddIngre)
          .then(function (response) {
            console.log("response", response);
            if(response.status == 200) {
              console.log("성공 응답", response.data);
              vm.$emit('hide');
              vm.$emit('update');
            }
          })
          .catch(function (e) {
            if(e.response.status == 400) {
              console.log("400 error");
            } else if(e.response.status == 500) {
              console.log("500 Unknown error");
            }
          });
      }
    },
    // 재료 필터
    ingredient_filter(){
      var inputVal;

      inputVal = document.getElementById("inputText").value;
      
      for (var i=0;i<this.ingredients.length;i++){
        if (Hangul.rangeSearch(this.ingredients[i].name, inputVal).length == 0){
          this.$refs.ingreName[i].classList.remove('visible');
        } else {
          this.$refs.ingreName[i].classList.add('visible');
        }
      }
    },
    // 재료 클릭 시 결정
    clickIngredient(payload){
      console.log(payload.srcElement.innerText);
      document.getElementById("inputText").value = payload.srcElement.innerText;

      this.name = payload.srcElement.innerText;
      
      for (var i=0;i<this.ingredients.length;i++){
        this.$refs.ingreName[i].classList.remove('visible');
      }
    },
    // 단위 필터
    units_filter(){
      for (var i=0;i<this.units.length;i++){
        this.$refs.unitsName[i].classList.add('visible');
      }

    },
    // 단위 클릭 시 결정
    clickUnit(payload){
      let vm = this;
      document.getElementById("inputUnit").value = " ";
      document.getElementById("inputUnit").value = payload.srcElement.innerText;
      vm.unit = payload.srcElement.innerText;
      for (var i=0;i<this.units.length;i++){
        this.$refs.unitsName[i].classList.remove('visible');
      }
      
    }
  }
}
</script>
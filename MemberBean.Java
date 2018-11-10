package test;  // 자바빈만 모아놓을 패키지, 생략가능
 
public class MemberBean 
{
    // 아이디, 비밀번호, 주소, 전화를 담을 프로퍼티(맴버변수)
    // 프로퍼티에 직접 접근할 수 없게 private를 사용한다.
    private String id;
    private String pw;
    private String addr;
    private String tel;
    
    /* 데이터를 가져오거나(get), 세팅하는(set)
    *  기능을 하는 메서드를 만든다.
    *  - 데이터를 가져오는 경우 - get메서드
    *  - 데이터를 세팅하는 경우 - set메서드
    */
    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getPw() {
        return pw;
    }
    public void setPw(String pw) {
        this.pw = pw;
    }
    public String getTel() {
        return tel;
    }
    public void setTel(String tel) {
        this.tel= tel;
    }
    public String getAddr() {
        return addr;
    }
    public void setAddr(String addr) {
        this.addr = addr;
    }    
}


출처: http://all-record.tistory.com/105 [세상의 모든 기록]
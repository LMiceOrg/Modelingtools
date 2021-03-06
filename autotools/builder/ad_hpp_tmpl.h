$def with (ctx)
/****************************************************************************
**
**  开发单位：$ctx['user_dept']
**  开发者：$ctx['user_name']
**  创建时间：$ctx['tm_now']
$if ctx.has_key('version'):
    **  版本号：$ctx['version']
$else:
    **  版本号：V1.0
$if ctx.has_key('h_name'):
    **  描述信息：$ctx['h_name']
$else:
    **  描述信息：$ctx['H_NAME']
****************************************************************************/


#ifndef $ctx['H_NAME']_TYPEDEFS_H_
#define $ctx['H_NAME']_TYPEDEFS_H_

#include <string>
#include <vector>
#include <map>
#include <string.h>

/** 全局类型别名 */
$if ctx.has_key('globaltypedefs'):
    namespace $ctx['autotools'].g_ns_name {


    $for key in ctx['globaltypedefs']:
        $#
        /** type: $key[0]
         * default: $key[2]
         */
        typedef $ctx['globaltypedefs'][key] $key[0];

    $# endfor
    } /* end of namespace $ctx['autotools'].g_ns_name */

$# endif global typedefs

/** 数组类型与别名 */
$if ctx.has_key('arraylist'):
    $ctx['arraylist']
$# endif arraylist



/** 全局宏定义 */
#define LMICE_STATIC_ASSERT(COND,MSG)       typedef char Error_##MSG[(!!(COND))*2-1]
#define LMICE_COMPILE_TIME_ASSERT4(X, W)    LMICE_STATIC_ASSERT(X,static_assertion_##W )
#define LMICE_COMPILE_TIME_ASSERT3(X, FUNC, LN) LMICE_COMPILE_TIME_ASSERT4(X, User_Must_Implement_##FUNC##_function_at_line_##LN)
#define LMICE_COMPILE_TIME_ASSERT2(X, f, l) LMICE_COMPILE_TIME_ASSERT3(X, f, l)
#define lmice_static_assert(X, func)        LMICE_COMPILE_TIME_ASSERT2(X, func, __LINE__)


namespace LMice {

//enum value is_pod
template<class _Tp, _Tp __v> struct cv {
    enum{ value =       __v};
    typedef _Tp         value_type;
    typedef cv          type;
};

// Default pod is 0
template<class T> struct is_pod:            public LMice::cv<int, 0>{};
// C POD types
template<> struct is_pod<wchar_t>:          public LMice::cv<int, 1>{};
template<> struct is_pod<signed char>:      public LMice::cv<int, 1>{};

template<> struct is_pod<char>:             public LMice::cv<int, 1>{};
template<> struct is_pod<short>:            public LMice::cv<int, 1>{};
template<> struct is_pod<int>:              public LMice::cv<int, 1>{};
template<> struct is_pod<int64_t>:          public LMice::cv<int, 1>{};

template<> struct is_pod<unsigned char>:    public LMice::cv<int, 1>{};
template<> struct is_pod<unsigned short>:   public LMice::cv<int, 1>{};
template<> struct is_pod<unsigned int>:     public LMice::cv<int, 1>{};
template<> struct is_pod<uint64_t>:         public LMice::cv<int, 1>{};

template<> struct is_pod<long double>:      public LMice::cv<int, 1>{};
template<> struct is_pod<double>:           public LMice::cv<int, 1>{};
template<> struct is_pod<float>:            public LMice::cv<int, 1>{};

// C++ POD types
template<> struct is_pod<bool>:             public LMice::cv<int, 1>{};

// User defined types
template<> struct is_pod<AppSim::Wstring255>:public LMice::cv<int, 1>{};


//可变长类型
template <class TSubClass, bool t>
struct LMPVector{

    inline int count() const {
        return count();
    }

    inline bool is_pod() const {
        return is_pod();
    }

    inline int size() const {
        return size();
    }

    inline int pack(char* buffer, int buffer_size) const {
        return pack(buffer, buffer_size);
    }

    inline int unpack(const char* buffer, int buffer_size) {
        return unpack(buffer, buffer_size);
    }

    inline void clear() {
        clear();
    }

    inline void push_back(const TSubClass& o) {
        push_back(o);
    }

    inline const TSubClass& operator[](size_t pos) const {
        return operator[](pos);
    }
    inline TSubClass& operator[](size_t pos) {
        return operator[](pos);
    }
};

template<class TSubClass>
struct LMPVector<TSubClass, true> {
    inline int count() const {
        return m_vec.size();
    }

    inline bool is_pod() const {
        return true;
    }

    inline int size() const {
        return sizeof(TSubClass)*m_vec.size() + sizeof(int)*2;
    }

    ///<[字节数] [数量] [数据项1],...[数据项n]
    inline int pack(char* buffer, int buffer_size) const {
        int ret = -1;
        int pos = 0;
        int sz = size();

        if(sz <= buffer_size) {
            ret = 0;

            memcpy(buffer + pos, &sz, sizeof(sz));
            pos += sizeof(sz);

            sz = count();
            memcpy(buffer + pos, &sz, sizeof(sz));
            pos += sizeof(sz);

            if(m_vec.size() > 0) {
                memcpy(buffer + pos, &m_vec[0], sizeof(TSubClass)*m_vec.size() );
            }

        }
        return ret;
    }

    inline int unpack(const char* buffer, int buffer_size) {
        int sz = 0;
        int pos = sizeof(int)*2;
        int i;
        int cnt = 0;

        m_vec.clear();

        if(buffer_size < pos)
            return -1;

        sz = *(const int*)buffer;
        cnt = *(const int*)(buffer+sizeof(int));

        if(sz > buffer_size) {
            return -1;
        }

        for(i=0; i<cnt; ++i) {
            TSubClass p;
            memcpy(&p, buffer+pos, sizeof(TSubClass));
            pos += sizeof(TSubClass);
            m_vec.push_back(p);
        }

        return 0;
    }

    inline void clear() {
        m_vec.clear();
    }

    inline void push_back(const TSubClass& o) {
        m_vec.push_back(o);
    }

    inline const TSubClass& operator[](size_t pos) const {
        return m_vec[pos];
    }

    inline TSubClass& operator[](size_t pos) {
        return m_vec[pos];
    }

    std::vector<TSubClass> m_vec;
};

template<class TSubClass>
struct LMPVector<TSubClass, false>{
    inline int count() const {
        return m_vec.size();
    }

    inline bool is_pod() const {
        return false;
    }

    inline int size() const {
        int sz = sizeof(int)*2;
        for(size_t i=0; i< m_vec.size(); ++i) {
            const TSubClass* pobj = &m_vec[i];
            sz += pobj->size();
        }
        return sz;
    }

    inline int pack(char* buffer, int buffer_size) const {
        int ret = -1;
        int pos = 0;
        int sz = size();

        if(sz <= buffer_size) {
            ret = 0;

            memcpy(buffer + pos, &sz, sizeof(sz));
            pos += sizeof(sz);

            sz = count();
            memcpy(buffer + pos, &sz, sizeof(sz));
            pos += sizeof(sz);

            for(size_t i = 0; i < m_vec.size(); ++i) {
                const TSubClass& obj = m_vec[i];
                obj.pack(buffer + pos, buffer_size);
                pos += obj.size();

            }
        }
        return ret;
    }

    inline int unpack(const char* buffer, int buffer_size) {
        int sz = 0;
        int pos = sizeof(int)*2;
        int i;
        int cnt = 0;

        m_vec.clear();

        if(buffer_size < pos)
            return -1;

        sz = *(const int*)buffer;
        cnt = *(const int*)(buffer+sizeof(int));

        if(sz > buffer_size) {
            return -1;
        }
        sz -= pos;
        for(i=0; i<cnt; ++i) {
            TSubClass p;
            p.unpack(buffer+pos, sz);
            pos += p.size();
            sz -= p.size();
            if(sz < 0) {
                return -1;
            }
            m_vec.push_back(p);
        }

        return 0;
    }

    inline void clear() {
        m_vec.clear();
    }

    inline void push_back(const TSubClass& o) {
        m_vec.push_back(o);
    }

    inline const TSubClass& operator[](size_t pos) const {
        return m_vec[pos];
    }

    inline TSubClass& operator[](size_t pos) {
        return m_vec[pos];
    }

    std::vector<TSubClass> m_vec;
};

//可变长类型
template <class TSubClass>
struct LMVector : public LMPVector<TSubClass, LMice::is_pod<TSubClass>::value>
{};

template <class TSubClass>
struct LMBaseClass
{
    typedef LMBaseClass<TSubClass>  this_type;

    inline int size() const {
        const TSubClass* p = static_cast<const TSubClass*>(this);
        return p->OnSize();
    }

    int OnSize() const {
        // 总是 返回 类型的大小
        //如果是可变长度类型，需要用户重载此函数
        lmice_static_assert(LMice::is_pod<TSubClass>::value, OnSize);
        return sizeof(TSubClass);
    }

    inline void swap(this_type& x) const {
        this_type c(x);
        x = *this;
        *this = c;
    }

    inline const char* data() const {
        // 只提供 POD类型时的访问
        lmice_static_assert(LMice::is_pod<TSubClass>::value, data);
        return reinterpret_cast<const char*>(this);

    }

    inline int pack(char* buffer, int buffer_size) const {
        const TSubClass* p = static_cast<const TSubClass*>(this);
        return p->OnPack(buffer, buffer_size);
    }

    int OnPack(char* buffer, int buffer_size) const {
        int ret = -1;
        // 非POD类型，以及buffer太小情况的pack处理，由用户实现处理
        lmice_static_assert(LMice::is_pod<TSubClass>::value, OnPack);
        if(size() <= buffer_size) {
            memcpy(buffer, (char*)this, size());
            ret = 0;
        }
        return ret;
    }

    inline int unpack(const char* buffer, int buffer_size) {
        TSubClass* p = static_cast<TSubClass*>(this);
        return p->OnUnpack(buffer, buffer_size);
    }

    int OnUnpack(const char* buffer, int buffer_size) {
        int ret = -1;
        // 非POD类型，以及buffer_size太小情况的unpack处理，由用户实现处理
        lmice_static_assert(LMice::is_pod<TSubClass>::value, OnUnpack);
        if(size() <= buffer_size) {
            memcpy((char*)this, buffer, size());
            ret = 0;
        }

        return ret;
    }


    inline bool is_pod() const {
        return LMice::is_pod<TSubClass>::value;
    }

    inline void clear() {
        TSubClass* p = static_cast<TSubClass*>(this);
        p->OnClear();
    }

    void OnClear() {
        //在POD类型时，调用memset初始化
        //非POD类型，用户重载此函数
        lmice_static_assert(LMice::is_pod<TSubClass>::value, OnClear);
        memset(this, 0, size());

    }



#if __cplusplus >= 199711L
    // c++0x 标准扩展
#endif

#if __cplusplus >= 201103L
    // c++11 标准扩展
protected:
    // 不允许直接实例化基类
    LMBaseClass() = default;
#endif

};

} /* end namespace LMice */

/** 各命名空间的枚举类型定义 */
$if ctx.has_key('enumlist'):
    $for key in ctx['enumlist']:
        #include "$key.lower()$'_enum.h'"

    $# endfor enumlist
$# endif enumlist

#endif // $ctx['H_NAME']_TYPEDEFS_H_

$def with (ctx)
$if not ctx.is_pod :
        int OnSize() const {

            return $ctx.size;
        }

        int OnPack(char* buffer, int buffer_size) const {
            int ret = -1;
            int pos = 0;
            if(size() <= buffer_size ) {
    $ctx.pack
                ret = 0;
            }
            return ret;
        }

        int OnUnpack(const char* buffer, int buffer_size) {
            int ret = -1;
            int pos = 0;
            if(size() <= buffer_size) {
    $ctx.unpack
                ret = 0;
            }

            return ret;
        }

        void OnClear() {
    $ctx.clear
        }

$else:
        //no need implement when struct is pod


// THIS IS AN AUTOMATICALLY GENERATED FILE.  DO NOT MODIFY
// BY HAND!!
//
// Generated by lcm-gen

#include <string.h>
#include "arc_control_t.h"

static int __arc_control_t_hash_computed;
static uint64_t __arc_control_t_hash;

uint64_t __arc_control_t_hash_recursive(const __lcm_hash_ptr *p)
{
    const __lcm_hash_ptr *fp;
    for (fp = p; fp != NULL; fp = fp->parent)
        if (fp->v == __arc_control_t_get_hash)
            return 0;

    __lcm_hash_ptr cp;
    cp.parent =  p;
    cp.v = __arc_control_t_get_hash;
    (void) cp;

    uint64_t hash = (uint64_t)0xcc5c654bac572c0dLL
         + __int64_t_hash_recursive(&cp)
         + __float_hash_recursive(&cp)
         + __float_hash_recursive(&cp)
        ;

    return (hash<<1) + ((hash>>63)&1);
}

int64_t __arc_control_t_get_hash(void)
{
    if (!__arc_control_t_hash_computed) {
        __arc_control_t_hash = (int64_t)__arc_control_t_hash_recursive(NULL);
        __arc_control_t_hash_computed = 1;
    }

    return __arc_control_t_hash;
}

int __arc_control_t_encode_array(void *buf, int offset, int maxlen, const arc_control_t *p, int elements)
{
    int pos = 0, element;
    int thislen;

    for (element = 0; element < elements; element++) {

        thislen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &(p[element].timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __float_encode_array(buf, offset + pos, maxlen - pos, &(p[element].motor), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __float_encode_array(buf, offset + pos, maxlen - pos, &(p[element].servo), 1);
        if (thislen < 0) return thislen; else pos += thislen;

    }
    return pos;
}

int arc_control_t_encode(void *buf, int offset, int maxlen, const arc_control_t *p)
{
    int pos = 0, thislen;
    int64_t hash = __arc_control_t_get_hash();

    thislen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &hash, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    thislen = __arc_control_t_encode_array(buf, offset + pos, maxlen - pos, p, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    return pos;
}

int __arc_control_t_encoded_array_size(const arc_control_t *p, int elements)
{
    int size = 0, element;
    for (element = 0; element < elements; element++) {

        size += __int64_t_encoded_array_size(&(p[element].timestamp), 1);

        size += __float_encoded_array_size(&(p[element].motor), 1);

        size += __float_encoded_array_size(&(p[element].servo), 1);

    }
    return size;
}

int arc_control_t_encoded_size(const arc_control_t *p)
{
    return 8 + __arc_control_t_encoded_array_size(p, 1);
}

int __arc_control_t_decode_array(const void *buf, int offset, int maxlen, arc_control_t *p, int elements)
{
    int pos = 0, thislen, element;

    for (element = 0; element < elements; element++) {

        thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &(p[element].timestamp), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __float_decode_array(buf, offset + pos, maxlen - pos, &(p[element].motor), 1);
        if (thislen < 0) return thislen; else pos += thislen;

        thislen = __float_decode_array(buf, offset + pos, maxlen - pos, &(p[element].servo), 1);
        if (thislen < 0) return thislen; else pos += thislen;

    }
    return pos;
}

int __arc_control_t_decode_array_cleanup(arc_control_t *p, int elements)
{
    int element;
    for (element = 0; element < elements; element++) {

        __int64_t_decode_array_cleanup(&(p[element].timestamp), 1);

        __float_decode_array_cleanup(&(p[element].motor), 1);

        __float_decode_array_cleanup(&(p[element].servo), 1);

    }
    return 0;
}

int arc_control_t_decode(const void *buf, int offset, int maxlen, arc_control_t *p)
{
    int pos = 0, thislen;
    int64_t hash = __arc_control_t_get_hash();

    int64_t this_hash;
    thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &this_hash, 1);
    if (thislen < 0) return thislen; else pos += thislen;
    if (this_hash != hash) return -1;

    thislen = __arc_control_t_decode_array(buf, offset + pos, maxlen - pos, p, 1);
    if (thislen < 0) return thislen; else pos += thislen;

    return pos;
}

int arc_control_t_decode_cleanup(arc_control_t *p)
{
    return __arc_control_t_decode_array_cleanup(p, 1);
}

int __arc_control_t_clone_array(const arc_control_t *p, arc_control_t *q, int elements)
{
    int element;
    for (element = 0; element < elements; element++) {

        __int64_t_clone_array(&(p[element].timestamp), &(q[element].timestamp), 1);

        __float_clone_array(&(p[element].motor), &(q[element].motor), 1);

        __float_clone_array(&(p[element].servo), &(q[element].servo), 1);

    }
    return 0;
}

arc_control_t *arc_control_t_copy(const arc_control_t *p)
{
    arc_control_t *q = (arc_control_t*) malloc(sizeof(arc_control_t));
    __arc_control_t_clone_array(p, q, 1);
    return q;
}

void arc_control_t_destroy(arc_control_t *p)
{
    __arc_control_t_decode_array_cleanup(p, 1);
    free(p);
}

int arc_control_t_publish(lcm_t *lc, const char *channel, const arc_control_t *p)
{
      int max_data_size = arc_control_t_encoded_size (p);
      uint8_t *buf = (uint8_t*) malloc (max_data_size);
      if (!buf) return -1;
      int data_size = arc_control_t_encode (buf, 0, max_data_size, p);
      if (data_size < 0) {
          free (buf);
          return data_size;
      }
      int status = lcm_publish (lc, channel, buf, data_size);
      free (buf);
      return status;
}

struct _arc_control_t_subscription_t {
    arc_control_t_handler_t user_handler;
    void *userdata;
    lcm_subscription_t *lc_h;
};
static
void arc_control_t_handler_stub (const lcm_recv_buf_t *rbuf,
                            const char *channel, void *userdata)
{
    int status;
    arc_control_t p;
    memset(&p, 0, sizeof(arc_control_t));
    status = arc_control_t_decode (rbuf->data, 0, rbuf->data_size, &p);
    if (status < 0) {
        fprintf (stderr, "error %d decoding arc_control_t!!!\n", status);
        return;
    }

    arc_control_t_subscription_t *h = (arc_control_t_subscription_t*) userdata;
    h->user_handler (rbuf, channel, &p, h->userdata);

    arc_control_t_decode_cleanup (&p);
}

arc_control_t_subscription_t* arc_control_t_subscribe (lcm_t *lcm,
                    const char *channel,
                    arc_control_t_handler_t f, void *userdata)
{
    arc_control_t_subscription_t *n = (arc_control_t_subscription_t*)
                       malloc(sizeof(arc_control_t_subscription_t));
    n->user_handler = f;
    n->userdata = userdata;
    n->lc_h = lcm_subscribe (lcm, channel,
                                 arc_control_t_handler_stub, n);
    if (n->lc_h == NULL) {
        fprintf (stderr,"couldn't reg arc_control_t LCM handler!\n");
        free (n);
        return NULL;
    }
    return n;
}

int arc_control_t_subscription_set_queue_capacity (arc_control_t_subscription_t* subs,
                              int num_messages)
{
    return lcm_subscription_set_queue_capacity (subs->lc_h, num_messages);
}

int arc_control_t_unsubscribe(lcm_t *lcm, arc_control_t_subscription_t* hid)
{
    int status = lcm_unsubscribe (lcm, hid->lc_h);
    if (0 != status) {
        fprintf(stderr,
           "couldn't unsubscribe arc_control_t_handler %p!\n", hid);
        return -1;
    }
    free (hid);
    return 0;
}

# ========================================================
# Stage: Final Image of 3x-ui
# ========================================================
FROM ubuntu:latest
ENV TZ=Asia/Tehran
WORKDIR /app

RUN apt-get update && apt-get install -y -q wget curl tar tzdata systemd ca-certificates fail2ban bash

RUN curl -sL https://raw.githubusercontent.com/IlyaChichkov/3x-ui/master/install.sh | bash

ENV X_UI_ENABLE_FAIL2BAN="true"
VOLUME [ "/etc/x-ui" ]
CMD [ "x-ui" ]
